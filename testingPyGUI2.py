#!/usr/local/bin/python3.6
import Tkinter as tk
from Tkinter import *
from PIL import Image #Needed to display video in GUI
from PIL import ImageTk #Needed to display video in GUI
#from Tkinter.tFileDialog import askopenfilename
import tkFileDialog
import sys
import os
import argparse
import time
import datetime
import imutils
import cv2


class StartWindow(tk.Tk):
	def __init__(self, parent=None):
		tk.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()
		
	def initialize(self):
		global runAnalysis
		global runPrediction
		global videoPath #Directory to load file
		global videoName #Name and extension of file
		global outputPath #Directory to store file(s)
		global defaultVid
		global trackingVid
		global otherVid1
		global otherVid2
		global filename
		global mainFrame
		
		
		self.grid()
		
		mainFrame = tk.Frame(self, bg='#66666E', relief='groove', bd=3)
		mainFrame.grid(row=0, rowspan=9, padx=5, pady=3)
		
		#A frame to hold script related widgets
		scriptFrame = tk.Frame(mainFrame, bg='#66666E')
		scriptFrame.grid(row=0, columnspan=2, padx=5, pady=3, sticky='w')
		
		#runAnalysis = IntVar()
		#cb1 = tk.Checkbutton(scriptFrame, text="Run Video Analysis", font=("Arial", 12, "bold"), variable=runAnalysis, width=15, padx=5, pady=3, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		#cb1.grid(row=0, column=0, sticky='w', padx=5, pady=3)
		
		#runPrediction = IntVar()
		#cb2 = tk.Checkbutton(scriptFrame, text="Run Prediction", font=("Arial", 12, "bold"), variable=runPrediction, width=15, padx=5, pady=3, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		#cb2.grid(row=0, column=1, sticky='w', padx=5, pady=3)
		
		#A frame to hold resource related widgets
		resourceFrame = tk.Frame(mainFrame, bg='#66666E')
		resourceFrame.grid(row=3, rowspan=3, column=0, sticky='w', padx=5, pady=3)
		
		#videoPath = StringVar()
		#e1_label = Label(resourceFrame, text='Enter video path:', anchor='nw', bg='#66666E', font=("Arial", 12, "bold"), fg='#FFFBFE')
		#e1_label.grid(row=0, column=0, sticky='e', padx=5, pady=3)
		#e1 = Entry(resourceFrame, textvariable = videoPath, width=50, bd=4, highlightbackground='#12100E', highlightthickness=2)
		#e1.grid(row=0, column=1)
		
		#A frame to hold video related widgets
		videoFrame = tk.Frame(mainFrame, bg='#66666E')
		videoFrame.grid(row=6, rowspan=2, columnspan=4, sticky='w', padx=5, pady=3)

		
		runButton = Button(mainFrame, text='Run', command=self.startEyes, bd=3, bg='#38383D', fg='#F2EFEA', font=("Arial", 12, "bold"), relief='ridge', overrelief='groove', activebackground='#38383D', activeforeground='#FFFCF7')
		runButton.grid(row=9, column=0, sticky='e', padx=5, pady=3)
		
		#A frame to hold the actual video
		imageFrame = tk.Frame(self, width=400, height=480, bd=5, relief='ridge', bg='#F2EFEA', highlightbackground='#12100E', highlightthickness=2)
		imageFrame.grid(row=1, column=2, padx=5, pady=5)
	
		runButton = Button(mainFrame, text='Prediction', command=self.readBrain, bd=3, bg='#38383D', fg='#F2EFEA', font=("Arial", 12, "bold"), relief='ridge', overrelief='groove', activebackground='#38383D', activeforeground='#FFFCF7')
		runButton.grid(row=9, column=2, sticky='e', padx=5, pady=3)
	
		

	def checkButtonSelection(self):
		if runAnalysis.get():
			#runEyes
			#chPath = videoPath.get()
			#os.chdir(chPath)
			#nameVideo = videoName.get()
			#print (nameVideo)
			#os.system('python eyes.py -v ' + nameVideo )	
			self.startEyes	
			runPrediction.set(0)
		elif runPrediction.get():
			#runBrain
			#chPath = videoPath.get()
			#os.chdir(chPath)
			os.system('python brain.py')
			runAnalysis.set(0)
			print("Brain")
	#Takes user inputs to run the "eyes" OpenCV portion of the code
	def runEyes(self):
		#if video name entered = null then video name entered = "none" 
		#chPath = videoPathEntered.get()
		#os.chdir(chPath)
		nameVideo = videoName.get()
		print (nameVideo)
		os.system('python eyes.py -v nameVideo')
	#Runs the output from eyes.py through the neural network for a prediction
	def runBrain(self):
		#chPath = videoPathEntered.get()
		#os.chdir(chPath)
		os.system('python brain.py')

	def startEyes(self):
		path = tkFileDialog.askopenfilename()
		if len(path) <= 0:
			camera = cv2.VideoCapture(0)
			time.sleep(0.30)
		else:
			camera = cv2.VideoCapture(path)
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
						print('|'.join(coordList))
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
			cv2.namedWindow("Security Feed")
			cv2.moveWindow("Security Feed", 720,90)
			cv2.imshow("Security Feed", frame)
			
			#cv2.imshow("Threshhold", thresh)
			#cv2.imshow("Frame Differences (MEDIAN BLUR)", frameDiffs)
			key = cv2.waitKey(1)
			if key == 27:
				camera.release()
				cv2.destroyAllWindows()
				break
		camera.release()
		cv2.destroyAllWindows()
		self.runBrain()
		

	def readBrain(self):

		#filename = "brainOutput.txt"
		#filepath = os.getcwd() + '/'
		#destination = filepath + filename
		#openFile = open(destination)
		fileP = open('brainOutput.txt') 
		line = fileP.readline()
		normal= float(0)
		abnormal=float(0)
		count = float(0)
		for line in fileP:
			if "normal" in line:
				normal += 1
				count += 1
			if "ABNORMAL" in line:
				abnormal += 1
				count += 1
	
		fileP.close()
		normalAvg = '{0:.0%}'.format(float((normal / count)))
		abnormalAvg = '{0:.0%}'.format(float((abnormal / count)))

		brainPredictionNormal = Label(mainFrame, text='noramlities: '+ normalAvg, bg='#66666E', font=("Arial", 16, "bold"), fg='#FFFBFE')
		brainPredictionNormal.grid(row=10, column=0, columnspan=4, sticky='w', padx=5, pady=3)
		brainPredictionAbnormal = Label(mainFrame, text='abnoramlities: '+ abnormalAvg, bg='#66666E', font=("Arial", 16, "bold"), fg='#FFFBFE')
		brainPredictionAbnormal.grid(row=11, column=0, columnspan=4, sticky='w', padx=5, pady=3)

		if abnormalAvg >= '50%':
			warning = Label(mainFrame, text='WARNING: LARGE AMOUNTS OF ABNORMAL BEHAVIOR HAS BEEN DETECTED, PLEASE CHECK SURVEILLANCE VIDEOS', bg='white', font=("Arial", 16, "bold"), fg='red')
			warning.grid(row=12, column=0, columnspan=4, sticky='w', padx=5, pady=3)

#Main loop of application		
if __name__ == '__main__':
	root = StartWindow(None)
	root.wm_title("Predictive Policing")
	root.wm_iconbitmap('Mocs.ico')
	root.resizable(False, False)
	root.configure(bg='#66666E')
	root.mainloop()
	
	
