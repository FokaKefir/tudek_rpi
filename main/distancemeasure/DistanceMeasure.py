import time
import constants_dm as CONSTANTS
import VL53L1X
from VibrationUnit import VibrationUnit
import RPi.GPIO as gpio
import smbus

def createUnits():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    
    setNewChannel(ch=CONSTANTS.I2C_CH_1)
    unitLeft = VibrationUnit(CONSTANTS.SENZOR_ADDRESS, CONSTANTS.I2C_CH_1, CONSTANTS.PORT_LEFT)
    
    setNewChannel(ch=CONSTANTS.I2C_CH_2)
    unitMid = VibrationUnit(CONSTANTS.SENZOR_ADDRESS, CONSTANTS.I2C_CH_2, CONSTANTS.PORT_MID)
    
    setNewChannel(ch=CONSTANTS.I2C_CH_3)
    unitRight = VibrationUnit(CONSTANTS.SENZOR_ADDRESS, CONSTANTS.I2C_CH_3, CONSTANTS.PORT_RIGHT)
    
    units = []
    units.append(unitLeft)
    units.append(unitMid)
    units.append(unitRight)
    
    
    return units

def calcPercent(dis):
    maxDis = CONSTANTS.INT_MAX_DISTANCE
    inverzPercent = (dis * 100) / maxDis
    percent = 100 - inverzPercent
    return percent

def sendInfoToGui(distances):
    strInfo = str(distances[0]) + "\n" + str(distances[1]) + "\n" + str(distances[2])
    try:
        fileDis = open("informations/distance.info", 'w')
        fileDis.write(strInfo)
        fileDis.close()
    except:
        pass

def readFromFile():
    strInfo = "open"
    try:
        fileRun = open("informations/run.info", "r")
        strInfo = fileRun.read()
        fileRun.close()
    except:
        print("cannot open the run.info file")
        
    return strInfo

def setNewChannel(unit=None, ch=None):
    if ch is None:
        channel = unit.getChannel()
        bus = smbus.SMBus(1)
        bus.write_byte(CONSTANTS.I2C_ADDRESS, channel)
    else:
        bus = smbus.SMBus(1)
        bus.write_byte(CONSTANTS.I2C_ADDRESS, ch)


def loop(units):
    cond = True
    while cond:
        distances = []
        for unit in units:
            setNewChannel(unit)
            distance = unit.getDistance()
            distances.append(distance)
            percent = calcPercent(distance)
            if percent < 0:
                unit.powerMotor(percent)
            else:
                unit.powerMotor(0)
                
            time.sleep(CONSTANTS.SLEEP_TIME)
            
        
        if readFromFile() == "close":
            cond = False
            
        sendInfoToGui(distances)
    

def closeUnits(units):
        
    gpio.cleanup()


if __name__ == "__main__":
    units = createUnits()
    loop(units)
    closeUnits(units)
    
    
    
    