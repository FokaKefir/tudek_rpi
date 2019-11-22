# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread
import importlib.util
import constants as CONSTANTS
import Audio

# If tensorflow is not installed, import interpreter from tflite_runtime, else import from regular tensorflow
pkg = importlib.util.find_spec('tensorflow')
if pkg is None:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    
    def __init__(self,resolution=(CONSTANTS.INT_CAMERA_RESOLUTION_WEIGHT, CONSTANTS.INT_CAMERA_RESOLUTION_HEIGHT),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

    # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
    # Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
    # Return the most recent frame
        return self.frame

    def stop(self):
    # Indicate that the camera and thread should be stopped
        self.stopped = True

# Define ImageRecognition class
class ImageRecognition:

    def __init__(self):
        None

    def loadAudio(self):
        self.audio = Audio.Audio()

    def loadTensorFlow(self):
    
        #Set the names
        self.modelName = CONSTANTS.STR_MODEL_NAME
        self.graphName = CONSTANTS.STR_GRAPH_NAME
        self.labelmapName = CONSTANTS.STR_LABELMAP_NAME
        self.objectsName = CONSTANTS.STR_OBJECTSMAP_NAME
        
        self.minConfThreshold = CONSTANTS.INT_MIN_CONF_TRESHOLD
        
        # Set the image height and weight from the constants file
        self.imW, self.imH = CONSTANTS.INT_CAMERA_RESOLUTION_WEIGHT , CONSTANTS.INT_CAMERA_RESOLUTION_HEIGHT
        
        # Get path to current working directory
        self.cwdPath = os.getcwd()
        
        # Path to .tflite file, which contains the model that is used for object detection
        self.pathToCkpt = os.path.join(self.cwdPath, self.modelName, self.graphName)
        
        # Path to label map file
        self.pathToLabels = os.path.join(self.cwdPath, self.modelName, self.labelmapName)
        
            # Path to the objects map file
        self.pathToObjects = os.path.join(self.cwdPath, self.modelName, self.objectsName)
        
        # Load the label map
        with open(self.pathToLabels, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
           
            # Load the objects map
        with open(self.pathToObjects, 'r') as g:
            self.myObjects = [line.strip() for line in g.readlines()]
        
        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is '???', which has to be removed.
        if self.labels[0] == '???':
            del(self.labels[0])
        
        # Load the Tensorflow Lite model and get details
        self.interpreter = Interpreter(model_path = self.pathToCkpt)
        self.interpreter.allocate_tensors()
        
        self.inputDetails = self.interpreter.get_input_details()
        self.outputDetails = self.interpreter.get_output_details()
        self.height = self.inputDetails[0]['shape'][1]
        self.width = self.inputDetails[0]['shape'][2]
        
        self.floatingModel = (self.inputDetails[0]['dtype'] == np.float32)
        
        self.inputMean = 127.5
        self.inputStd = 127.5
        
        # Initialize frame rate calculation
        self.frameRateCalc = 1
        self.freq = cv2.getTickFrequency()
        
        # Initialize video stream
        self.videostream = VideoStream(resolution=(self.imW, self.imH), framerate=30).start()
        time.sleep(1)
    
    def putInFrame(self):
        # Get bounding box coordinates and draw box
        # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
        i = self.i
        self.ymin = int(max(1,(self.boxes[i][0] * self.imH)))
        self.xmin = int(max(1,(self.boxes[i][1] * self.imW)))
        self.ymax = int(min(self.imH,(self.boxes[i][2] * self.imH)))
        self.xmax = int(min(self.imW,(self.boxes[i][3] * self.imW)))
                    
        cv2.rectangle(self.frame, (self.xmin, self.ymin), (self.xmax, self.ymax), (10, 255, 0), 2)
        
        # Draw label
        self.object_name = self.labels[int(self.classes[i])] # Look up object name from "labels" array using class index
        self.label = '%s: %d%%' % (self.object_name, int(self.scores[i]*100)) # Example: 'person: 72%'
        self.labelSize, self.baseLine = cv2.getTextSize(self.label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
        self.label_ymin = max(self.ymin, self.labelSize[1] + 10) # Make sure not to draw label too close to top of window
        cv2.rectangle(self.frame, (self.xmin, self.label_ymin - self.labelSize[1]-10), (self.xmin + self.labelSize[0], self.label_ymin + self.baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
        cv2.putText(self.frame, self.label, (self.xmin, self.label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
    
    def openWindow(self):
        # Draw framerate in corner of frame
        cv2.putText(self.frame,'FPS: {0:.2f}'.format(self.frameRateCalc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        
        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', self.frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            self.cond = False
    
    
    def calculatingImageSize(self):
        
        i = self.i
        x = self.boxes[i][3] - self.boxes[i][1]
        y = self.boxes[i][2] - self.boxes[i][0]
        return x*y
        
        
    def loop(self):
        
        self.cond = True
        
        #for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        while self.cond:
        
            # Start timer (for calculating frame rate)
            self.t1 = cv2.getTickCount()
        
            # Grab frame from video stream
            self.frame1 = self.videostream.read()
        
            # Acquire frame and resize to expected shape [1xHxWx3]
            self.frame = self.frame1.copy()
            self.frameRGB = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frameResized = cv2.resize(self.frameRGB, (self.width, self.height))
            self.inputData = np.expand_dims(self.frameResized, axis=0)
        
            # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
            if self.floatingModel:
                self.inputData = (np.float32(self.inputData) - self.inputMean) / self.inputStd
        
            # Perform the actual detection by running the model with the image as input
            self.interpreter.set_tensor(self.inputDetails[0]['index'], self.inputData)
            self.interpreter.invoke()
        
            # Retrieve detection results
            self.boxes = self.interpreter.get_tensor(self.outputDetails[0]['index'])[0] # Bounding box coordinates of detected objects
            self.classes = self.interpreter.get_tensor(self.outputDetails[1]['index'])[0] # Class index of detected objects
            self.scores = self.interpreter.get_tensor(self.outputDetails[2]['index'])[0] # Confidence of detected objects
            #num = interpreter.get_tensor(outputDetails[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)
        
            # Loop over all detections and draw detection box if confidence is above minimum threshold
            strNewAudioWord = None
            intSize = 0.0
            for self.i in range(len(self.scores)):
                if ((self.scores[self.i] > self.minConfThreshold) and (self.scores[self.i] <= 1.0)):
                    self.putInFrame()
                    
                    actuallyObjectName = self.labels[int(self.classes[self.i])]
                    actuallySize = self.calculatingImageSize()
                    if (self.myObjects.count(str(actuallyObjectName))) and (actuallySize > intSize):
                        strNewAudioWord = actuallyObjectName
                        intSize = actuallySize
                        
        
            self.openWindow()
            
            # Calculate framerate
            self.t2 = cv2.getTickCount()
            self.time1 = (self.t2 - self.t1)/self.freq
            self.frameRateCalc = 1/self.time1
            
            if intSize != 0:
                strOut = str(intSize) + " " + strNewAudioWord
                print(strOut)
                self.audio.say(strNewAudioWord)
                time.sleep(CONSTANTS.INT_WAIT_TIME_SECOND)
        
            
        
        # Clean up
        cv2.destroyAllWindows()
        self.videostream.stop()
        
        
def main():
    imageRecognition = ImageRecognition()
    imageRecognition.loadAudio()
    imageRecognition.loadTensorFlow()
    imageRecognition.loop()
    
    
    
    
main()
    
    
    
    
