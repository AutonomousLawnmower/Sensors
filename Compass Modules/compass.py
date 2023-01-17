import py_qmc5883l

class Compass:
    def __init__(self):
        self.sensor = py_qmc5883l.QMC5883L()
    
    def getDirection():
        m = sensor.get_magnet()
        print(m)
        
    #Need to look into calibration