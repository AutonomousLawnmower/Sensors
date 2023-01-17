from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
data0 = 12
data1 = 16
data2 = 18
data3 = 22
data4 = 24
data5 = 26
data6 = 32
data7 = 36

GPIO.setup(data0,GPIO.IN)
GPIO.setup(data1,GPIO.IN)
GPIO.setup(data2,GPIO.IN)
GPIO.setup(data3,GPIO.IN)
GPIO.setup(data4,GPIO.IN)
GPIO.setup(data5,GPIO.IN)
GPIO.setup(data6,GPIO.IN)
GPIO.setup(data7,GPIO.IN)

class Ultrasonic(object):
    
    def get_distance(self):
        if GPIO.input(data0)==0:
            x0 = 0
        else:
            x0 = 1
        
        if GPIO.input(data1)==0:
            x1 = 0
        else:
            x1 = 2
            
        if GPIO.input(data2)==0:
            x2 = 0
        else:
            x2 = 4
            
        if GPIO.input(data3)==0:
            x3 = 0
        else:
            x3 = 8    
        
        if GPIO.input(data4)==0:
            x4 = 0
        else:
            x4 = 16
          
        if GPIO.input(data5)==0:
            x5 = 0
        else:
            x5 = 32    
    
        if GPIO.input(data6)==0:
            x6 = 0
        else:
            x6 = 64
          
        if GPIO.input(data7)==0:
            x7 = 0
        else:
            x7 = 128
        

        return(x0+x1+x2+x3+x4+x5+x6+x7)
    
