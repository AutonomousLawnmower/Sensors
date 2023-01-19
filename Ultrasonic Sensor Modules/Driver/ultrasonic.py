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

select0 = 38
select1 = 40

dataBits = [data0, data1, data2, data3, data4, data5, data6]
selectBits = [select0, select1]

GPIO.setup(dataBits,GPIO.IN)
GPIO.setup(data7,GPIO.IN)

GPIO.setup(selectBits,GPIO.OUT)


class Ultrasonic:
    def get_distance(self, s0 = 0, s1 = 0): #this
        GPIO.output(select0, s0) #(pin#, value)
        GPIO.output(select1, s1)
        #possible delay
        distance = 0
        for i, bit in enumerate(dataBits):
            distance += GPIO.input(bit)<<i
            
        overflow = bool(GPIO.input(data7))
        
        return(distance, overflow)
    
    