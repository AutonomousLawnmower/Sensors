from compass import Compass
import time
from ultrasonic import Ultrasonic
import RPi.GPIO as GPIO

def determineRelDir(angle, refCompass):
    for direction, value in refCompass.items():
        if (value-23 < angle <= value + 23):
            return direction
    while True:
        print("IDK:", angle)
    return 'IDK'

def getRelDir(northDir):
    directions = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
    compass = {}
    tempDir = northDir-90
    if tempDir < 0:
        tempDir+360
        
    for direct in directions:
        compass[direct] = tempDir
        tempDir+=45
        if tempDir >= 360:
            tempDir-=360
    
    return compass
def main():
    compass = Compass()
    directions = getRelDir(compass.getDirection())
    print(directions)
    us = Ultrasonic()
    try:
        while True:
            time.sleep(.1)
            dirValue = compass.getDirection()
            currentDirection = determineRelDir(dirValue, directions)
            #print(dirValue-directions['E'])
            print(f'Current Direction: {currentDirection}')
            
            distance, overflow = us.get_distance()
            
            if (distance < 30 and not overflow):
                if (currentDirection == 'E'):
                    print('Turning LEFT')
                elif (currentDirection == 'W'):
                    print("Turning RIGHT")
    except Exception as e:
        print(e)
        GPIO.cleanup()
main()
