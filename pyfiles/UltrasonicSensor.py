import RPi.GPIO as gpio
import time
import signal
import sys
import os
import constants as CONSTANTS
import tty
import curses
import getch 


gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

units = [(CONSTANTS.ECHO_A, CONSTANTS.TRIG_A, CONSTANTS.MOTOR_A, CONSTANTS.GPIO_MOTOR_NAME_A),
          (CONSTANTS.ECHO_B, CONSTANTS.TRIG_B, CONSTANTS.MOTOR_B, CONSTANTS.GPIO_MOTOR_NAME_B),
          (CONSTANTS.ECHO_C, CONSTANTS.TRIG_C, CONSTANTS.MOTOR_C, CONSTANTS.GPIO_MOTOR_NAME_C)]

maxDistance = CONSTANTS.INT_MAX_DISTANCE
def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    gpio.cleanup()
    sys.exit(0)

def initWidget(echo, trig, motor, motorName):
    signal.signal(signal.SIGINT, close)

    # set GPIO input and output channels
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    gpio.setup(motor, gpio.OUT)

    gpio.output(trig, False)
    gpio.output(motor, False)
    
    strPwmActivate = "gpio mode " + str(motorName) + " pwm"
    
    os.popen(strPwmActivate)
    motorOff(motorName)
    
    

def initWidgets():
    for unit in units:
        if(unit[0] != 0):
            
            initWidget(unit[0], unit[1], unit[2], unit[3])
            
    time.sleep(0)
    os.popen("gpio readall")


def measure(echo, trig):
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)
    
    while gpio.input(echo)==False:
        pulseStart = time.time()
    
    while gpio.input(echo)==True:
        pulseEnd = time.time()
        
    
    pulseDuration = pulseEnd - pulseStart

    distance = pulseDuration * CONSTANTS.INT_SOUND_SPEED
    
    distance = round(distance, 2)
    
    return distance


def motorOff(motorName):
    strCommand = "gpio pwm " + str(motorName) + " 0"
    os.popen(strCommand)


def motorOn(motorName, percent):
    pwm = (CONSTANTS.INT_MAX_PWM * percent) / 100
    strCommand = "gpio pwm " + str(motorName) + " " + str(pwm)
    os.popen(strCommand)
    

def turnUpMotor(distance, motor, motorName):
    
    if distance<maxDistance+10:
        percent = int(int(distance/10) * 10)
        print("Distance: ", distance, "cm")
        percentOn = maxDistance - percent
        print("On: ", percentOn)
        
        motorOn(motorName, percentOn)
        
        
    else:
        motorOff(motorName)
        
    


def loop():

    chrPressed = 0
    while True:

        for unit in units:
            if(unit[0] != 0):
                distance = measure(unit[0], unit[1])
                
                turnUpMotor(distance, unit[2], unit[3])
                
        #TODO making a mode how to close the program
                
        

        
    
def main():
    initWidgets()
    
    loop()
    gpio.cleanup()
    
    
main()
    
    