import py_qmc5883l

class Compass:
    def __init__(self):
        self.sensor = py_qmc5883l.QMC5883L(output_range = py_qmc5883l.RNG_8G)
        self.sensor.mode_continuous()
        self.sensor.declination = 11
        self.NORTH = self.getDirection()
        if self.NORTH == None:
            self.NORTH = 90
    
    def getDirection(self, display = False):
        data = self.sensor.get_bearing()
        if display:
            print(data)
        return data
        
    def getRelDir(self):
        current = self.getDirection()
        tempDir=0
        if current is not None:
            tempDir = current-self.NORTH+90
        if tempDir < 0:
            tempDir+360
        elif tempDir>=360:
            tempDir - 360
        return tempDir
            
    def determineRelDir(self, angle, refCompass):
        for direction, value in refCompass.items():
            if (value-23 < angle <= value + 23):
                return direction

    '''def getRelDir(self):
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
        
        return compass'''
        
if __name__ == '__main__':
    compass = Compass()
    while True:
        
        compass.getDirection(True)