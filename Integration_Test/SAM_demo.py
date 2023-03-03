from sensors.compass import *
from sensors.motorControl import *
from sensors.ultrasonic import *
from ml.detect_picam32 import *

import threading, time

us = Ultrasonic()
motorCTRL = MotorController("/dev/ttyAMA0")
compass = Compass()

sensorData = {'Compass':0, 'US0':0, 'Ov0':False, 'US1':0, 'Ov1':False}
mlData = {'Grass Detected':False, 'Bounding Box':None}
motorCMD = None

sensorLock = threading.Lock()
motorLock = threading.Lock()
mlLock = threading.Lock()

def sensorDataAcq():
    while True:
        with sensorLock:
            us1, ov1 = us.get_distance(1,0)
            us0, ov0 = us.get_distance(0,0)
            
            sensorData['Compass'] = compass.getDirection()
            sensorData['US0'] = us0
            sensorData['Ov0'] = ov0
            sensorData['US1'] = us1
            sensorData['Ov1'] = ov1
            
def motorControl():
    while True:
        if (motorCMD != None):                  #if there is a command
            with motorLock:                     #aquire lock
                motorCTRL.sendCommand(motorCMD) #send command
                motorCMD = None                 #clear command

def mlDataAcq():
    args = initML()
    runML(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,int(args.numThreads), mlData, mlLock)
      
def start(threads):
    for t in threads:
        t.start()

def stop(threads):
    for t in threads:
        t.kill()
    endML()

if __name__ == '__main__':
    threads = [threading.Thread(target=sensorDataAcq), threading.Thread(motorControl),
               threading.Thread(mlDataAcq)]
    start(threads)
        
    try:
        while True:
            with sensorLock:
                print(sensorData)

            with mlLock:
                print(mlData)

            #Turn
            with motorLock:
                motorCMD = FORWARD
            time.sleep(5)
            with motorLock:
                motorCMD = LEFT
            time.sleep(1)
    except KeyboardInterrupt:
        stop(threads)