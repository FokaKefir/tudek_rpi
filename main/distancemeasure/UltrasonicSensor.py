import RPi.GPIO as gpio
import time
import signal
import sys
import os
import constants_dm as CONSTANTS
import tty
import curses



gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

units = [(CONSTANTS.ECHO_A, CONSTANTS.TRIG_A, CONSTANTS.MOTOR_A, None),
          (CONSTANTS.ECHO_B, CONSTANTS.TRIG_B, CONSTANTS.MOTOR_B, None),
          (CONSTANTS.ECHO_C, CONSTANTS.TRIG_C, CONSTANTS.MOTOR_C, None)]
pwm = [None, None, None]
maxDistance = CONSTANTS.INT_MAX_DISTANCE
def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    gpio.cleanup()
    sys.exit(0)

def initWidget(unit, index):
    signal.signal(signal.SIGINT, close)

    echo = unit[0]
    trig = unit[1]
    motor = unit[2]

    # set GPIO input and output channels
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    gpio.setup(motor, gpio.OUT)

    gpio.output(trig, False)
    gpio.output(motor, False)
    
    motorPwm = gpio.PWM(motor, 100)
    motorPwm.start(0)
    
    motorTurn(motorPwm, 0)
    
    pwm[index] = motorPwm

def initWidgets():
    i = 0
    for unit in units:
        if(unit[0] != 0):
            
            initWidget(unit, i)
        i = i+1    
    time.sleep(0)
    print("INFO: Initialized GPIO widgets.")


def measure(echo, trig):
    gpio.output(trig, True)
    time.sleep(0.00001)
    gpio.output(trig, False)
    
    pulseStart = 0
    
    while gpio.input(echo)==False:
        pulseStart = time.time()
    
    while gpio.input(echo)==True:
        pulseEnd = time.time()
        if ((pulseEnd - pulseStart) > CONSTANTS.MAX_TIME):
            return -1
        
    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * CONSTANTS.INT_SOUND_SPEED
    distance = round(distance, 2)
    
    return distance


def motorTurn(motorName, percent):
    #print(percent)
    motorName.ChangeDutyCycle(percent)
     
def getPercent(distance):
    calcPercent = (distance * 100) / maxDistance
    return calcPercent
          

def controllingMotor(distance, motor, motorPwm):
    
    if distance<=maxDistance and distance != -1:
        percent = getPercent(distance)
        
        percentOn = 100 - percent
        
        motorTurn(motorPwm, percentOn)
        
    else:
        
        motorTurn(motorPwm, 0)
    


def loop():

    chrPressed = 0
    while True:
        i=0
        for unit in units:
            if(unit[0] != 0):
                distance = measure(unit[0], unit[1])
                #print("Distance: ", distance, "cm")
                
                controllingMotor(distance, unit[2], pwm[i])
                
            time.sleep(CONSTANTS.SLEEP_TIME) 
            i = i+1
           
        #TODO making a mode how to close the program
                
        

        
    
def main():
    initWidgets()
    
    loop()
    gpio.cleanup()
    
    
main()
    
    
