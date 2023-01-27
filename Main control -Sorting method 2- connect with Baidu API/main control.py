#coding:utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')

from aip import AipImageClassify
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import json

APP_ID = '20457028'
API_KEY = 'HEPzpDvjK1DrEte0TRjER2UR'
SECRECT_KEY = 'qDIRA2mAL4yM7xeZPXqnvHfAXnWeSuWM'

cilent = AipImageClassify(APP_ID, API_KEY, SECRECT_KEY)	

camera = PiCamera()
ServoPin1 = 21
ServoPin2 = 20
PWMFreq = 50
Trig_Pin = 4
Echo_Pin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(ServoPin1, GPIO.OUT)
GPIO.setup(ServoPin2, GPIO.OUT)
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Echo_Pin, GPIO.IN)

#camera function
def getImage():
    #set the resolution of picture, smaller means fatster upload but bad accuracy
    camera.resolution = (1024,768)
    #begin shoot
    camera.start_preview()	
    print ('==Shooting image')
    #wait 2 sce to ensure camera have a good condition
    time.sleep(2)
    #shoot and storage
    camera.capture('Image.jpg')	
    time.sleep(2)
    print ('==Shoot successful')

#request baidu server
def apiRequest(image):
    #upload picture to baidu's server with application object
    print ('==Uploading image to server')
    returnedResult = cilent.advancedGeneral(image)
    print ('==Returing results')
    #build stander json format 
    json_str = json.dumps(returnedResult)
    #load json inmormation to memory
    jsonResult = json.loads(json_str)
    #decode jason and pick what we need
    result = jsonResult['result'][0]['keyword']
    return result

#trash classify list
def trashList(result):
    if result == 'Plastic':
        return 0
    elif result == 'Battery':
        return 1
    elif result == 'napkin':
        return 2
    elif result == 'apple':
        return 3
    elif result == '?':
        return err('SRY, picture is not good enough to distinguish, plz try again!')
    #if trash didnt list upown, it will be classified in TYPE 2 
    else:
        return 2

#Print error message and exit function or application        
def err(err_msg):
    print ('\033[1;30;41m!!!!!!!!WARNING!!!!!!!!\033[0m')
    print (err_msg)
    print ('\033[1;30;41m!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
    print ('==Exiting function!')

#main function, call this function and return type of trash
#meaning of returnd value
#===0----Plastic
#===1---- battery
#===2----napkin
#===3----apple
def trashClassify():
    print('==Preparp tp distinguish')
    getImage()
    img = open('Image.jpg', 'rb').read()
    result = apiRequest(img)
    trash_type = trashList(result)
    print ('==========')
    print ('==This is :')
    print (result)
    print ('==========')
    print ('==Type is :')
    print (trash_type)
    print ('==========')
    print ('==Finish!')
    return trash_type

#motor control
def motorCtrl(duty1, duty2):
    pwm1.ChangeDutyCycle(duty1)
    pwm2.ChangeDutyCycle(duty2)
    time.sleep(2)
    pwm1.ChangeDutyCycle(7.5)
    pwm2.ChangeDutyCycle(7)

#SORTING
def trashThrow(trash_type):
    pwm1 = GPIO.PWM(ServoPin1, PWMFreq)
    pwm2 = GPIO.PWM(ServoPin2, PWMFreq)
    pwm1.start(0)
    pwm2.start(0)
    pwm1.ChangeDutyCycle(7.3)
    pwm2.ChangeDutyCycle(7.3)
    if trash_type == 1:
        motorCtrl(2.5, 7)
    if trash_type == 2:
        motorCtrl(12.5, 7)
    if trash_type == 3:
        motorCtrl(2.5, 10.5)
    if trash_type == 4:
        motorCtrl(12.5, 10.5)

#Acquire distance
def getDistance():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    return (t2 - t1) * 340 * 100 / 2

#main
if __name__ == '__main__':
    try:
        while True:
            if getDistance() < 300:
                print ('==Trash has been putted in!')
                trash_type = trashClassify()
                trashThrow(trash_type)
                time.sleep(1.5)           
            else:
                print ('==Waitting......')
                pass
    except KeyboardInterrupt:
        GPIO.cleanup()
