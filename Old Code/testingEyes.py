#!/usr/local/bin/python2.7
import Eyes2
from Eyes2 import Eyes
#import brain2
#from brain2 import Brain

eye = Eyes("abnormal.mp4", "Capstone/Classes")
print(eye.vidName)
eye.startEyes()
#brain = Brain()
#brain.runBrain()
