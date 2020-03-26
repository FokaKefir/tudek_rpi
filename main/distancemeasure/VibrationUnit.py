import VL53L1X
import RPi.GPIO as gpio
import constants_dm as CONSTANTS

class VibrationUnit:
    
    def __init__(self, senzorAddress, channel, gpioPort=None):
        self.channel = channel
        
        self.senzor = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=CONSTANTS.SENZOR_ADDRESS)
        self.senzor.open()
        self.port = gpioPort
        self.distance = None
        
        gpio.setup(self.port, gpio.OUT)
        
        self.motor = gpio.PWM(self.port, 100)
        self.motor.start(0)
        self.powerMotor(0)
        
        
    def getDistance(self):
        
        self.senzor.start_ranging(2)
        
        dis = self.senzor.get_distance() / 10
        
        self.senzor.stop_ranging()
        
        return dis
        
    def powerMotor(self, percent):
        return
        self.motor.ChangeDutyCycle(percent)
        
    def getChannel(self):
        return self.channel
        

        
        