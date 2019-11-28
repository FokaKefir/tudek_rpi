import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)

myMotor = 21
gpio.setup(myMotor, gpio.OUT)
motorName = gpio.PWM(myMotor, 100)
motorName.start(0)
def motorTurn(motorName, percent):
    motorName.ChangeDutyCycle(percent)
    
def main():
    while(1):
        print(myMotor)
        
        motorTurn(motorName, 50)
        time.sleep(0.5)    
    
    
main()