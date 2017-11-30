#!/usr/local/bin/python3.6
import Tkinter as tk
from Tkinter import *
from PIL import Image #Needed to display video in GUI
from PIL import ImageTk #Needed to display video in GUI
import tkFileDialog
import sys
import os
import argparse
import time
import datetime
import imutils
import cv2
import threading #Needed to display video in GUI

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
		global imageFrame
		
		self.grid()
		self.thread = None
		self.panel = None
		self.stopEvent = None

		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.startEyes, args=())
		#self.thread.start()
		
		mainFrame = tk.Frame(self, bg='#66666E', relief='groove', bd=3)
		mainFrame.grid(row=0, rowspan=9, padx=5, pady=3)
		
		#A frame to hold script related widgets
		scriptFrame = tk.Frame(mainFrame, bg='#66666E')
		scriptFrame.grid(row=0, columnspan=2, padx=5, pady=3, sticky='w')
		
		runAnalysis = IntVar()
		cb1 = tk.Checkbutton(scriptFrame, text="Run Video Analysis", font=("Arial", 12, "bold"), variable=runAnalysis, width=15, padx=5, pady=3, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		cb1.grid(row=0, column=0, sticky='w', padx=5, pady=3)
		
		runPrediction = IntVar()
		cb2 = tk.Checkbutton(scriptFrame, text="Run Prediction", font=("Arial", 12, "bold"), variable=runPrediction, width=15, padx=5, pady=3, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		cb2.grid(row=0, column=1, sticky='w', padx=5, pady=3)
		
		#A frame to hold resource related widgets
		resourceFrame = tk.Frame(mainFrame, bg='#66666E')
		resourceFrame.grid(row=3, rowspan=3, column=0, sticky='w', padx=5, pady=3)
		
		videoPath = StringVar()
		e1_label = Label(resourceFrame, text='Enter video path:', anchor='nw', bg='#66666E', font=("Arial", 12, "bold"), fg='#FFFBFE')
		e1_label.grid(row=0, column=0, sticky='e', padx=5, pady=3)
		e1 = Entry(resourceFrame, textvariable = videoPath, width=50, bd=4, highlightbackground='#12100E', highlightthickness=2)
		e1.grid(row=0, column=1)
		
		outputPath = StringVar()
		e2_label = Label(resourceFrame, text='Enter an output path:', bg='#66666E', font=("Arial", 12, "bold"), fg='#FFFBFE')
		e2_label.grid(row=1, column=0, sticky='e', padx=5, pady=3)
		e2 = Entry(resourceFrame, textvariable = outputPath, width=50, bd=4, highlightbackground='#12100E', highlightthickness=2)
		e2.grid(row=1, column=1, sticky='w')
		
		videoName = StringVar()
		e3_label = Label(resourceFrame, text='Enter filename and extension:', bg='#66666E', font=("Arial", 12, "bold"), fg='#FFFBFE')
		e3_label.grid(row=2, column=0, sticky='e', padx=5, pady=3)
		e3 = Entry(resourceFrame, textvariable = videoName, width=50, bd=4, highlightbackground='#12100E', highlightthickness=2)
		e3.grid(row=2, column=1, sticky='w')

		#A frame to hold video related widgets
		videoFrame = tk.Frame(mainFrame, bg='#66666E')
		videoFrame.grid(row=6, rowspan=2, columnspan=4, sticky='w', padx=5, pady=3)
		
		e4_label = Label(videoFrame, text='Choose one or more of the following to view...', bg='#66666E', font=("Arial", 16, "bold"), fg='#FFFBFE')
		e4_label.grid(row=0, column=0, columnspan=4, sticky='w', padx=5, pady=3)
		
		defaultVid = IntVar()
		c4 = Checkbutton(videoFrame, text='Default', font=("Arial", 12, "bold"), variable = defaultVid, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		c4.grid(row=1, column=0, sticky='w', padx=5, pady=3)

		trackingVid = IntVar()
		c5 = Checkbutton(videoFrame, text='Tracking ', font=("Arial", 12, "bold"), variable = trackingVid, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		c5.grid(row=1, column=1, sticky='w', padx=5, pady=3)

		otherVid1 = IntVar()
		c6 = Checkbutton(videoFrame, text='Other', font=("Arial", 12, "bold"), variable = otherVid1, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		c6.grid(row=1, column=2, sticky='w', padx=5, pady=3)

		otherVid2 = IntVar()
		c7 = Checkbutton(videoFrame, text='Other', font=("Arial", 12, "bold"), variable = otherVid2, bg='#66666E', fg='#FFFBFE', selectcolor='#38383D')
		c7.grid(row=1, column=3, sticky='w', padx=5, pady=3)
		
		runButton = Button(mainFrame, text='Run', command=self.startEyes(), bd=3, bg='#38383D', fg='#F2EFEA', font=("Arial", 12, "bold"), relief='ridge', overrelief='groove', activebackground='#38383D', activeforeground='#FFFCF7')
		runButton.grid(row=9, column=0, sticky='e', padx=5, pady=3)
		
		#A frame to hold the actual video
		imageFrame = tk.Frame(self, width=600, height=500, bd=5, relief='ridge', bg='#F2EFEA', highlightbackground='#12100E', highlightthickness=2)
		imageFrame.grid(row=1, column=2, padx=5, pady=5)
	
	#Determines which script to run depending on checkbox selection	
	def checkButtonSelection(self):
		if runAnalysis.get():
			#self.runEyes
			self.startEyes()
			runPrediction.set(0)
			print("Eyes")
		elif runPrediction.get():
			#runBrain
			runAnalysis.set(0)
			print("Brain")
	
	#Takes user inputs to run the "eyes" OpenCV portion of the code
	def runEyes(self):
		chPath = videoPathEntered.get()
		os.chdir(chPath)
		nameVideo = videoName.get()
		os.system('python eyes.py -v nameVideo')
	
	#Runs the output from eyes.py through the neural network for a prediction
	def runBrain(self):
		chPath = videoPathEntered.get()
		os.chdir(chPath)
		os.system('python brain.py')
	
	def startEyes(self):
		path = tkFileDialog.askopenfilename()
		if len(path) <= 0:
			camera = cv2.VideoCapture(0)
			time.sleep(0.05)
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
		try:
		# start reading video stream
			while not self.stopEvent.is_set():
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
								#now = datetime.datetime.now()
								#current_time = now.isoformat()
								#filename = 'PSP' + current_time
								#filepath = '/home/fef/nn/output/'
									filename = 'PSP_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f") + '.txt'
									filepath = os.getcwd() + '\\'
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
				cv2.imshow("Security Feed", frame)
				image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				if self.panel is None:
					self.panel = tk.Label(image = image)
					self.panel.image = image
					self.panel.grid(row = 0, column = 0)
				else:
					self.panel.configure(image = image)
					self.panel.image = image
				#cv2.imshow("Threshhold", thresh)
				#cv2.imshow("Frame Differences (MEDIAN BLUR)", frameDiffs)
				key = cv2.waitKey(10)
				if key == ord("q"):
					break
		except RuntimeError, e:
			print("this not working")
		# cleanup the camera and close any open windows
		camera.release()
		cv2.destroyAllWindows()
		self.stopEvent.set()

		
#Main loop of application		
if __name__ == '__main__':
	root = StartWindow(None)
	root.wm_title("Predictive Policing")
	root.wm_iconbitmap('Mocs.ico')
	root.resizable(False, False)
	root.configure(bg='#66666E')
	root.mainloop()