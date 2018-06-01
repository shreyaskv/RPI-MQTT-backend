from app import db

class Controls(db.Document):
    name = db.StringField(max_length=80, unique = True)
    controlStatus = db.FloatField(min_value = 0 ,max_value = 1)
    control_id = db.StringField(max_length=20)

class Rooms(db.Document):
    name = db.StringField(max_length=80, unique =True)
    controls = db.ListField(db.ReferenceField(Controls), default=[])

class ControlsCollection(db.Document):
    group = db.StringField(max_length = 80, unique = True)
    rooms = db.ListField(db.ReferenceField(Rooms),default = [])

class Time(db.Document):
    start = db.IntField()
    stop = db.IntField()

class AccessGroup(db.Document):
    name = db.StringField(max_length=80, unique = True)
    UIDs = db.ListField(db.StringField(), default=[])
    accessibleControlIDs = db.ListField(db.StringField(), default=[])
    accessTime = db.ListField(db.ReferenceField(Time), default=[])



class User(db.Document):
    email = db.StringField(max_length=255, unique = True)
    accessGroup = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    picture = db.StringField()
    userExpiry = db.StringField()
    userID = db.StringField()
    name = db.StringField(max_length=255)
    refreshSecret = db.LongField()
    roles = db.StringField()

class Role(db.Document):
    name = db.StringField(max_length=80, unique = True)
    description = db.StringField(max_length=255)

'''
class Wifi(db.Document):
    ssid = db.StringField()
    password = db.StringField()

'''






