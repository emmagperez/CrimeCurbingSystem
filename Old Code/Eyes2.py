# import the necessary packages
#!/usr/local/bin/python2.7
import argparse
import imutils
import time
import cv2
import numpy
import datetime
import os

class Eyes:

    def __init__(self, vidName, outputPath):
        self.vidName = vidName
        self.outputPath = outputPath
    
    def startEyes(self):
        if self.vidName == "none" :
            camera = cv2.VideoCapture(0)
            time.sleep(0.30)
        else:
            camera = cv2.VideoCapture(self.vidName)
        # initialize first frame    
        (grabbed, frame) = camera.read()    
        firstFrame = frame
        firstFrame = imutils.resize(firstFrame, width=500)
        firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
        count = 0
        lastSeenCount = 0 
        coordList = []

        # start reading video stream
        while True:
            (grabbed, frame) = camera.read()    
            count += 1
            frame = imutils.resize(frame, width=500)        #resize frames so they are all the same size for comparison
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  #convert frame to grayscale
            frameDiffs = cv2.absdiff(firstFrame, gray)      #find differences between frame and the first frame
            frameDiffs = cv2.medianBlur(frameDiffs, 5)      #blur outlines a bit
            _,thresh = cv2.threshold(frameDiffs, 20, 255, cv2.THRESH_BINARY)    #convert to black and white
            _,contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #identify objects as contours

            #determine rectangle size and draw rectangles on the frame
            #for cnt in contours:

            for  i in range (0, len(contours)):
                if(cv2.contourArea(contours[i]) > 50):
                    (x, y, w, h) = cv2.boundingRect(contours[i])
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
                    xCoord = int(round(x + (.5 * w))/10)
                    yCoord = int(round(y + (.5 * h))/10)

                    if count%3 == 0:
                      if ((count - lastSeenCount) > 20):
                        coordList = []
                        lastSeenCount = count
                        tup = (str(xCoord), str(yCoord))
                        coordList.append(' '.join(tup))
                        #print coordList
                        print '|'.join(coordList)
                        if len(coordList) > 4:
                            now = datetime.datetime.now()
                            current_time = now.isoformat()
                            filename = 'PSP' + current_time
                            filepath = '/home/fef/nn/output/'
                            destination = filepath + filename
                            f = open(filename, 'w')
                            f.write('|'.join(coordList))
                            f.close()  # you can omit in most cases as the destructor will call it
                            #os.rename(filename, destination)
                            coordList = []
                    cv2.rectangle(frame,(xCoord,yCoord),(xCoord,yCoord),(0,0,255),3)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    #cv2.putText(frame, str(i) ,(x,y+h), font, 2,(255,255,255),1,cv2.LINE_AA)
            #show various frames
            cv2.imshow("Security Feed", frame)
            cv2.imshow("Threshhold", thresh)
            cv2.imshow("Frame Differences (MEDIAN BLUR)", frameDiffs)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()
