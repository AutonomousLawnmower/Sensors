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

mode_Forward = 0
mode_TurnLeft = 1
mode_TurnRight = 2

def sensorDataAcq():
    while True:
        us1, ov1 = us.get_distance(1,0)
        us0, ov0 = us.get_distance(0,0)
        
        sensorData['Compass'] = compass.getDirection()
        sensorData['US0'] = us0
        sensorData['Ov0'] = ov0
        sensorData['US1'] = us1
        sensorData['Ov1'] = ov1
            
def motorControl():
    global motorCMD
    while True:
        if (motorCMD != None):              #if there is a command
            motorCTRL.sendCommand(motorCMD) #send command
            motorCMD = None                 #clear command

def mlDataAcq():
    args = initML('ml/grass1.tflite')
    runML(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,int(args.numThreads), mlData)
      
def start(threads):
    for t in threads:
        t.start()

def stop(threads):
    #for t in threads:
    #    t.kill()
    endML()
    
def circle(refTime):
    if (motorCMD == LEFT and time.time()-refTime > 1):
        cmd = FORWARD
        refTime = time.time()
    elif (motorCMD == FORWARD and time.time()-refTime > 5):
        cmd = LEFT
        refTime = time.time()
    else:
        cmd = FORWARD
    return cmd, refTime

def zigzag(mode, refTime, step):
    cmd = FORWARD
    newMode = mode
    nextStep = step
    
    if (mode == mode_Forward):
        if (sensorData['US0'] < 20 and not(sensorData['Ov0'])):
            newMode = mode_TurnRight if (0 <= compass.getRelDir() <=180) else mode_TurnLeft
            refTime = time.time()
    
    elif (mode == mode_TurnRight):
        if step == 0:
            if (time.time() - refTime < 1):
                cmd = RIGHT
            else:
                nextStep = 1
                refTime = time.time()
        elif step == 1:
            if (time.time() - refTime < 1):
                cmd = FORWARD
            else:
                nextStep = 2
                refTime = time.time()
        elif step == 2:
            if (time.time() - refTime < 1):
                cmd = RIGHT
            else:
                nextStep = 0
                newMode = mode_Forward
                refTime = time.time()
            
    elif (mode == mode_TurnLeft):
        if step == 0:
            if (time.time() - refTime < 1):
                cmd = LEFT
            else:
                nextStep = 1
                refTime = time.time()
        elif step == 1:
            if (time.time() - refTime < 1):
                cmd = FORWARD
            else:
                nextStep = 2
                refTime = time.time()
        elif step == 2:
            if (time.time() - refTime < 1):
                cmd = LEFT
            else:
                nextStep = 0
                newMode = mode_Forward
                refTime = time.time()
    else:
        cmd = FORWARD
    return cmd, newMode, refTime, nextStep

if __name__ == '__main__':
    threads = [threading.Thread(target=sensorDataAcq), threading.Thread(target = motorControl),
               threading.Thread(target = mlDataAcq)]
    start(threads)
    stop_mower = True
    refTime = time.time()
    motorCMD = STOP
    mMode = mode_Forward
    step = 0
    try:
        while True:
            motorCMD, mMode, refTime, step = zigzag(mMode, refTime, step)
                
    except KeyboardInterrupt:
        motorCMD = STOP
        stop(threads)