import time
import constants_dm as CONSTANTS
import VL53L1X
from VibrationUnit import VibrationUnit


if __name__ == "__main__":
    unit = VibrationUnit(0x29)
    for _ in range(10):
        
        dis = unit.getDistance()
        print(dis, end=" cm\n")
        
    unit.closeSenzor