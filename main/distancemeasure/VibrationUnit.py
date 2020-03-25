import VL53L1X
import RPi.GPIO as gpio
import constants_dm as CONSTANTS

class VibrationUnit:
    
    def __init__(self, senzorAddress, gpioPort=None):
        self.senzor = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=senzorAddress)
        self.senzor.open()
        self.senzor.start_ranging(2)
        
        self.port = gpioPort
        self.distance = None
        
        
    def getDistance(self):
        return self.senzor.get_distance() / 10
        
    def closeSenzor(self):
        self.senzor.stop_ranging()