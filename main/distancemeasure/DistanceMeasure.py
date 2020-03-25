import time
import constants_dm as CONSTANTS
import VL53L1X
from VibrationUnit import VibrationUnit

def createUnits():
    
    unitLeft = VibrationUnit(CONSTANTS.ADDRESS_LEFT, CONSTANTS.PORT_LEFT)
    unitMid = VibrationUnit(CONSTANTS.ADDRESS_MID, CONSTANTS.PORT_MID)
    unitRight = VibrationUnit(CONSTANTS.ADDRESS_RIGHT, CONSTANTS.PORT_RIGHT)
    
    units = [unitLeft, unitMidm unitRight]
    return units

def loop(units):
    pass


def closeUnits(units):
    for unit in units:
        unit.closeSenzor()
        
    gpio.cleanup()


if __name__ == "__main__":
    units = createUnits()
    loop(units)
    closeUnits(units)
    
    
    
    