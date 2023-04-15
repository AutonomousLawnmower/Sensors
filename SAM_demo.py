from sensors.compass import *
from sensors.motorControl import *
from sensors.ultrasonic import *
from sensors.pico import *
from ml.detect_picam32 import *

import threading, time

#Create subsystems
us = Ultrasonic()
motorCTRL = MotorController("/dev/ttyAMA0")
pico = Pico("/dev/ttyAMA2")
compass = Compass()

#Data Varaibles
sensorData = {'Compass':0, 'US0':0, 'Ov0':False, 'US1':0, 'Ov1':False}
mlData = {'Grass Detected':False, 'Bounding Box':None}
motorCMD = None

#Constants
mode_Forward = 0
mode_TurnLeft = 1
mode_TurnRight = 2

#Shared Shutdown Var
stop = [False]

#Global Vars for acceleration
xpos = 0
ypos = 0

def picoData():
    global motorCMD, xpos, ypos
    while True:
        if stop[0] == True:
            return
        
        #Parse Data
        data = pico.getdata()
        data = data.split(',')
        
        if len(data) >= 5:
            #Estimate Velocity
            dx = float(data[2]) - xpos 
            dy = float(data[3]) - ypos
            
            #Change speed to MAX if it is moving too slowly (on incline or in hole)
            motorCMD = SPEDMAX if (abs(dx) < 0.1 and abs(dy) < 0.1) else SPEDNORM
            xpos = float(data[2])
            ypos = float(data[3])
        time.sleep(1)

def sensorDataAcq():
    while True:
        if stop[0] == True:
            return
        
        #Aquire data from ultrasonics
        us1, ov1 = us.get_distance(1,0)
        us0, ov0 = us.get_distance(0,0)
        
        #Store data
        sensorData['Compass'] = compass.getDirection()
        sensorData['US0'] = us0
        sensorData['Ov0'] = ov0
        sensorData['US1'] = us1
        sensorData['Ov1'] = ov1
            
def motorControl():
    global motorCMD
    while True:
        if stop[0] == True:
            return
        if (motorCMD != None):              #if there is a command
            motorCTRL.sendCommand(motorCMD) #send command
            motorCMD = None                 #clear command

def mlDataAcq():
    args = initML('ml/grass1.tflite')
    runML(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,int(args.numThreads), mlData, stop)
      
def start(threads):
    for t in threads:
        t.start()

def stop_threads(threads):
    global stop
    stop[0] = True
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
    global motorCMD
    cmd = FORWARD
    newMode = mode  #Overall mode
    nextStep = step #Steps in mode (if applicable)
    
    if (mode == mode_Forward):
        cmd = FORWARD
        motorCMD = BSTART
        if ((not (mlData['Grass Detected'])) or (sensorData['US0'] < 30 and not(sensorData['Ov0']))): #if obstacle or no grass
            newMode = mode_TurnLeft if sensorData['Compass'] >= 180 else mode_TurnRight #Turn depending on orientation
            nextStep = -1
            
    elif (mode == mode_TurnRight): #STOP, RIGHT, FORWARD, RIGHT
        if step == -1:
            if (time.time() - refTime < 1):
                cmd = STOP
            else:
                nextStep = 0
                refTime = time.time()
        elif step == 0:
            if (time.time() - refTime < 0.5):
                cmd = RIGHT
            else:
                nextStep = 1
                refTime = time.time()
        elif step == 1:
            if (time.time() - refTime < 0.5):
                cmd = FORWARD
            else:
                nextStep = 2
                refTime = time.time()
        elif step == 2:
            if (time.time() - refTime < 0.5):
                cmd = RIGHT
            else:
                nextStep = -1
                newMode = mode_Forward
                refTime = time.time()
            
    elif (mode == mode_TurnLeft): #STOP, LEFT, FORWARD, LEFT
        if step == -1:
            if (time.time() - refTime < 1):
                cmd = STOP
            else:
                nextStep = 0
                refTime = time.time()
        elif step == 0:
            if (time.time() - refTime < 0.5):
                cmd = LEFT
            else:
                nextStep = 1
                refTime = time.time()
        elif step == 1:
            if (time.time() - refTime < 0.5):
                cmd = FORWARD
            else:
                nextStep = 2
                refTime = time.time()
        elif step == 2:
            if (time.time() - refTime < 0.5):
                cmd = LEFT
            else:
                nextStep = -1
                newMode = mode_Forward
                refTime = time.time()
        
    return cmd, newMode, refTime, nextStep

if __name__ == '__main__':
    threads = [threading.Thread(target=sensorDataAcq), threading.Thread(target = motorControl),
               threading.Thread(target = mlDataAcq), threading.Thread(target = picoData)]
    start(threads)
    stop_mower = True
    refTime = time.time()
    motorCMD = STOP
    time.sleep(.1)
    motorCMD = SPEDNORM
    time.sleep(.1)
    mMode = mode_Forward
    BLADEON = True
    motorCMD = STOP
    time.sleep(.1)
    
    step = -1
    try:
        while True:
            motorCMD, mMode, refTime, step = zigzag(mMode, refTime, step)
                
    except KeyboardInterrupt:
        motorCMD = STOP
        time.sleep(1)
        stop_threads(threads)
        time.sleep(5)