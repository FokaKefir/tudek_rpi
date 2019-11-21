import os

class Audio:
    
    def __init__(self):
        None

    def say(self, text):
        os.popen('espeak "'+text+'" --stdout | aplay 2>/dev/null')
    
    
    