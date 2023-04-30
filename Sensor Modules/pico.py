import serial
import time

class Pico:
    serialPort = None
    
    def __init__(self, port):
        self.port_setup(port)
    
    def port_setup(self, port = "/dev/ttyAMA2"):
        self.serialPort = serial.Serial(port, baudrate=115200, timeout=2)

    def getdata(self, decode = True):
        self.serialPort.write(bytearray('1', 'utf-8'))
        data = self.serialPort.readline()
        if decode:
            data= data.decode()
        return data
    
    def resetdata(self):
       self.serialPort.write(bytearray('2', 'utf-8')) 
        
if __name__ == "__main__":
    pico = Pico("/dev/ttyAMA2")
    
    while True:
        try:
            time.sleep(.2)
            print(pico.getdata())

        except KeyboardInterrupt: #End Program
            break