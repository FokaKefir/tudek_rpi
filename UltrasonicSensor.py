import RPi.GPIO as gpio
import time
import signal
import sys
import constants as CONSTANTS



gpio.setmode(gpio.BCM)

units = [(CONSTANTS.ECHO_A, CONSTANTS.TRIG_A, CONSTANTS.MOTOR_A),
          (CONSTANTS.ECHO_B, CONSTANTS.TRIG_B, CONSTANTS.MOTOR_B),
          (CONSTANTS.ECHO_C, CONSTANTS.TRIG_C, CONSTANTS.MOTOR_C)]

def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    gpio.cleanup()
    sys.exit(0)

def initWidgets():
    signal.signal(signal.SIGINT, close)

    # set GPIO input and output channels
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)

    gpio.output(trig, False)

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

def turnUpMotor(distance)
    
    if distance<200:
        print("Distance: ", distance, "cm")
    time.sleep(CONSTANTS.INT_SLEEP_TIME)

def loop():

    while True:

        for unit in units:
            distance = measure(unit[0], unit[1])
            turnUpMotor(distance)

        
    
def main():
    initWidgets()
    loop()
    
    
main()
    
    