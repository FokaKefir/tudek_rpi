import time
import constants_dm as CONSTANTS
import VL53L1X
from VibrationUnit import VibrationUnit

def createUnits():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    
    unitLeft = VibrationUnit(CONSTANTS.ADDRESS_LEFT, CONSTANTS.PORT_LEFT)
    unitMid = VibrationUnit(CONSTANTS.ADDRESS_MID, CONSTANTS.PORT_MID)
    unitRight = VibrationUnit(CONSTANTS.ADDRESS_RIGHT, CONSTANTS.PORT_RIGHT)
    
    units = [unitLeft, unitMidm unitRight]
    return units

def calcPrecent(dis):
    maxDis = CONSTANTS.INT_MAX_DISTANCE
    inverzPrecent = (dis * 100) / maxDis
    percent = 100 - inverzPercent
    return percent




def loop(units):
    cond = True
    while cond:
            
    
        for unit in units:
            distance = unit.getDistance()
            percent = calcPercent(distance)
            if percent < 0:
                unit.powerMotor(percent)
            else:
                unit.powerMotor(0)
                
            time.sleep(CONSTANTS.SLEEP_TIME)
            


def closeUnits(units):
    for unit in units:
        unit.closeSenzor()
        
    gpio.cleanup()


if __name__ == "__main__":
    units = createUnits()
    loop(units)
    closeUnits(units)
    
    
    
    