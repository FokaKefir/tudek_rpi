import RPi.GPIO as gpio
import time
import signal
import sys
import constants as CONSTANTS



gpio.setmode(gpio.BCM)

units = [(CONSTANTS.ECHO_A, CONSTANTS.TRIG_A, CONSTANTS.MOTOR_A),
          (CONSTANTS.ECHO_B, CONSTANTS.TRIG_B, CONSTANTS.MOTOR_B),
          (CONSTANTS.ECHO_C, CONSTANTS.TRIG_C, CONSTANTS.MOTOR_C)]

maxDistance = CONSTANTS.INT_MAX_DISTANCE
times = int(CONSTANTS.INT_SLEEP_TIME / CONSTANTS.INT_WPM_TIME)
def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    gpio.cleanup()
    sys.exit(0)

def initWidget(echo, trig, motor):
    signal.signal(signal.SIGINT, close)

    # set GPIO input and output channels
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    gpio.setup(motor, gpio.OUT)

    gpio.output(trig, False)
    gpio.output(motor, False)    

def initWidgets():
    for unit in units:
        if(unit[0] != 0):
            
            initWidget(unit[0], unit[1], unit[2])
            
    time.sleep(5)


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

def turnUpMotor(distance, motor):
    
    if distance<maxDistance+10:
        percent = int(int(distance/10) * 10)
        print("Distance: ", distance, "cm")
        print("Percent: ", percent, "%")
        percentOn = maxDistance - percent
        percentOff = maxDistance - percentOn
        print("On: ", percentOn, ", Off: ", percentOff)
        
        
        for i in range(times):
            gpio.output(motor, True)
            time.sleep(CONSTANTS.INT_WPM_TIME * percentOn)
            gpio.output(motor, False)
            time.sleep(CONSTANTS.INT_WPM_TIME * percentOff)
        
    
    

def loop():

    while True:

        for unit in units:
            if(unit[0] != 0):
                distance = measure(unit[0], unit[1])
                turnUpMotor(distance, unit[2])
                
        time.sleep(CONSTANTS.INT_SLEEP_TIME)

        
    
def main():
    initWidgets()
    loop()
    
    
main()
    
    