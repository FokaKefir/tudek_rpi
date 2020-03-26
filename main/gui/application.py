import tkinter as tk
from tkinter import *
import time
import os

def stop():
    win.destroy()

def updateStrings():
    try:
        fileDistance = open("informations/distance.info", "r")
    
        distanceLeft = fileDistance.readline()
        distanceCenter = fileDistance.readline()
        distanceRight = fileDistance.readline() + '\n'

        strDistanceLeft.set(distanceLeft + " cm")
        strDistanceCenter.set(distanceCenter + " cm")
        strDistanceRight.set(distanceRight + " cm")
    
        fileDistance.close()
    except:
        pass
    
    try:
        
        fileObject = open("informations/object.info", "r")
        obejct = fileObject.read()
        strObject.set("Obejct: " + obejct)
        fileObject.close()
    except:
        pass

def updateRunFile(strOut):
    while True:
        try:
            fileRun = open("informations/run.info", "w")
            fileRun.write(strOut)
            fileRun.close()
            break
        except:
            pass


def clearFiles():
    try:
        fileObject = open("informations/object.info", "w")
        fileObject.write("")
        fileObject.close()
    except:
        pass
    
    
    try:
        fileDistance = open("informations/distance.info", "w")
        fileDistance.write("")
        fileDistance.close()
    except:
        pass

win = tk.Tk()
win.title("Informations")

strDistanceLeft = StringVar()
strDistanceCenter = StringVar()
strDistanceRight = StringVar()
strObject = StringVar()

Label(win, text="Left distance").grid(row=0, column=0)
Label(win, text="Center distance").grid(row=0, column=1)
Label(win, text="Right distance").grid(row=0, column=2)
labelLeft = Label(win, text="0 cm", textvariable=strDistanceLeft).grid(row=1, column=0)
labelCenter = Label(win, text="0 cm", textvariable=strDistanceCenter).grid(row=1, column=1)
labelRight = Label(win, text="0 cm", textvariable=strDistanceRight).grid(row=1, column=2)
labelObject = Label(win, text="Object: ?", textvariable=strObject).grid(row=2, column=0)
button = tk.Button(win, text="Stop", command=lambda: stop()).grid(row=2, column=2)

currentPath = os.path.dirname(__file__)

print("Windows is open.")
updateRunFile("open")

while True:
    updateStrings()
    try:
        win.update()
    except :
        
        print("Windows is closed.")
        updateRunFile("close")
        break
    
time.sleep(1)  
clearFiles()
