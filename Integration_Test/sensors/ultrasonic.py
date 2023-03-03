from time import sleep
import RPi.GPIO as GPIO

data0 = 12
data1 = 16
data2 = 18 #18
data3 = 22 #22
data4 = 24
data5 = 26
data6 = 32
data7 = 36 #36

select0 = 38
select1 = 40

#dataBits = [data0, data1, data2, data3, data4]

dataBits = [data0, data1, data2, data3, data4, data5, data6]
selectBits = [select0, select1]


class Ultrasonic:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(dataBits,GPIO.IN)
        GPIO.setup(data7,GPIO.IN)
        GPIO.setup(selectBits,GPIO.OUT)
        
    def get_distance(self, s0 = 0, s1 = 0, binary = False): #this
        GPIO.output(select0, s0) #(pin#, value)
        GPIO.output(select1, s1)
        #possible delay
        distance = 0
        distanceSTR = ""
        for i, bit in enumerate(dataBits):
            value = GPIO.input(bit)
            distance += value << i
            distanceSTR += str(value)
            
        overflow = bool(GPIO.input(data7))
        if not binary:
            return(distance, overflow)
        else:
            return(distance, distanceSTR, overflow)

if __name__ == '__main__':
    us = Ultrasonic()
    while True:
        for i in range(0,2):
            distance, disSTR, overflow = us.get_distance(i,0, True)
            print(f"Sensor:{i}\tDistance: {distance}\tBits: {disSTR}\tOverflow:{overflow}")
        sleep(1)