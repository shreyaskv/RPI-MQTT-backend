from app import app
from models import Role,Rooms,User,AccessGroup,Controls,ControlsCollection,Time
from flask import request, jsonify
import random
import time
import jwt
from oauth2client import crypt, client

flow = client.flow_from_clientsecrets('client_secret.json',scope='profile',redirect_uri='http://www.example.com/oauth2callback')
flow.params['access_type'] = 'offline'         # offline access
flow.params['include_granted_scopes'] = True   # incremental auth

CLIENT_ID = "25667199244-6vrfmn6kif5psmu2p8q3t8v5q9701sat.apps.googleusercontent.com"
QRKey = 'mhUfnCAM2gid8PomMTP25c8N9xVsGRHYX5NwQfMPZpVhDWttj0kpqpYwIpk2LnX1GFpLD8ohG1a6GMkTcfd6y3uvD7sdXawvoC5Tdau2IK4f8SkamnaZ9qUgXiDL'
secret = 'mhUfnCAM2gid8PomMTP25c8N9xVsGRHYX5NwQfMPZpVhDWttj0kpqpYwIpk2LnX1GFpLD8ohG1a6GMkTcfd6y3uvD7sdXawvoC5Tdau2IK4f8SkamnaZ9qUgXiDL'

@app.route('/login', methods=['POST'])
def login():
    content=request.get_json(force=True)                 #QRKey and idToken
    token=content['idToken']
    qrToken = content['qrToken']
    qrKey = jwt.decode(qrToken,'secret')
    print(token)
    try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        return jsonify({'result':'fail','message':'failed at idtoken verification'})

    print(idinfo['email'])

    if not User.objects(email=idinfo['email']):
        if User.objects(roles = 'admin'):
            print('Login Failed----User Not Found')
            return jsonify({"result":"fail","message":"User Not Found"})
        else :
            print("First User Creation")
            if qrKey == QRKey:
                refreshKey = random.getrandbits(32)
                try:
                    user = User(email=idinfo['email'], refreshSecret = refreshKey, userExpiry = 'Never', roles = 'admin')
                    user.save()
                except:
                    print("Email already used")
                    return jsonify({"result":"fail","message":"Email already exists"})
                refreshToken = jwt.encode({'refreshSecret':refreshKey,'email':idinfo['email']}, SECRET_KEY, algorithm = 'HS256')
                return jsonify({"message":refreshToken, "result":"success"})
            else:
                print("Fail---Go back to Login")
                return jsonify({"result":"fail","message":"Fail---Go back to Login"})

    else :
        user = User(email=idinfo['email'])
        refreshKey = user.refreshSecret
        refreshToken = jwt.encode({'refreshSecret': refreshKey, 'email': idinfo['email']}, SECRET_KEY, algorithm='HS256')
        return jsonify({"message":refreshToken, "result":"success"})



@app.route('/getAccessToken', methods=['POST'])
def getAccessToken():
    content = request.get_json(force=True)
    print(content)
    refreshToken = content['refreshToken']
    payload = jwt.decode(refreshToken, SECRET_KEY)
    print(payload['refreshSecret'])
    user = User.objects(refreshSecret=payload['refreshSecret'])

    if not user:
        print("fail")
        return jsonify({"message":"fail"})
    else:
        secs = int(time.time())
        accessToken = jwt.encode({'email': payload['email'],'exp': secs + 360}, SECRET_KEY,algorithm='HS256')
        return accessToken

@app.route('/createControl',methods = ['POST'])
def createControlMethod():
    content = request.get_json()
    if Controls.objects(name = content['name'] , roomGroup = content['roomGroup']):
        return jsonify({"message":"fail"})
    else:
        control = Controls(name = content['name'], roomGroup = content['roomGroup'], controlStatus = content['controlStatus'], myid = content['myid'])
        control.save()
        #mqtt.subscribe(content['roomGroup']/content['name'])
        #@mqtt.on_message()
        #def handle_mqtt_message(client, userdata, message):
        #    data = dict(
        #        topic=message.topic,
        #        payload=message.payload.decode()
        #    )
        return jsonify({"message":"Control Created"})
