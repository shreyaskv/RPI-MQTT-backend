
import I2C_LCD_driver
import RPi.GPIO as GPIO
from time import *

from matrixKeypad_RPi_GPIO import keypad
#from matrixKeypad_RPi_GPIO import keypad
from time import sleep

mylcd = I2C_LCD_driver.lcd()
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize the keypad class
kp = keypad()

def UnLock():
  mylcd.lcd_display_string(" Lock Opened", 1)
  GPIO.setup(11, GPIO.OUT)

  GPIO.output(11, GPIO.HIGH)
  sleep(5)
  GPIO.output(11, GPIO.LOW)

  return None

def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
	x=GPIO.input(26)
        if(x==True):
                print("HIGH")
                mylcd.lcd_clear()
                UnLock()
                sleep(0.5)
                mylcd.lcd_display_string("Enter code: ", 1)
        r = kp.getKey()
    return r

while(True):

        mylcd.lcd_display_string("Enter code: ", 1)

        d1 = digit()

        mylcd.lcd_display_string(str(d1), 2,0)
        sleep(0.5)

        d2 = digit()
        mylcd.lcd_display_string(str(d2), 2,1)
        sleep(0.5)

        d3 = digit()
        mylcd.lcd_display_string(str(d3), 2,2)
        sleep(0.5)

        d4 = digit()
 	mylcd.lcd_display_string(str(d4), 2,3)
        sleep(0.5)
        # printing out the assembled 4 digit code.
        print "You Entered %s%s%s%s "%(d1,d2,d3,d4)

        if(d1==1 and d2==0 and d3==0 and d4==8):
                mylcd.lcd_clear()
                UnLock()

        else:
		mylcd.lcd_display_string("Wrong passcode", 1)
                sleep(1)
                mylcd.lcd_clear()



