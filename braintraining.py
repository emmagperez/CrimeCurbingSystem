# LSTM with Variable Length Input Sequences to One Character Output
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import glob
import os 

mypath = '/home/fef/nn/output/'

#model = load_model('testmodel.h5')
# fix random seed for reproducibility
numpy.random.seed()
# prepare the dataset of input to output pairs 
num_inputs = 20000
num_tests = 50
max_len = 5
min_seq_len = 4
max_seq_len = 5
max_value = 50
max_velocity = 8
batch_size = 5
num_epochs = 2
xCoordArray = []
yCoordArray = []
dataX = []
dataY = []
dataX2 = []
dataY2 = []
for i in range(num_inputs):
	startFuzz = (numpy.random.random()) -.5
	#print startFuzz
	start = numpy.random.randint(0,max_value)
	start += startFuzz
	#print start
	#velocity = numpy.random.randint(-(max_velocity),max_velocity+1)
	velocity = (numpy.random.random()) * max_velocity
	velocity -= 4
	#print velocity
	seq_len = numpy.random.randint(min_seq_len, max_seq_len)
	sequence_in = []
	for i in range (0, seq_len):
		fuzz = ((numpy.random.random())/2) -.25
		#print fuzz
		point = (int(round(start + (i * velocity)+ fuzz)))
		sequence_in.append(point)
	#print sequence_in
	sequence_out = []
	lastPoint = int(round((sequence_in[-1] + velocity)))
	if lastPoint < 0:
		lastPoint = 0
	#if lastPoint > 50:
	#	lastPoint = 50
	sequence_out.append(lastPoint)
	#print lastPoint
	dataX.append(sequence_in)
	dataY.append(sequence_out) 
#print "Sequence Out:"
#print dataY
#print "Artificial Input"
#print dataX
#print len(dataX)
#print dataY
#print len(dataY)
#print ""

#dataX = []
#dataY = []

""" 
file_list = glob.glob('PSP*')

file_list.sort()
#print "\n".join(file_list)
#os.remove('/home/fef/nn/output/deletthis')
if len(file_list) > 0:
	for i in file_list:
		f = open(i, 'r')
		#print file_list[0]
		dataArray = f.read().split('|')
		for i in dataArray:
			separate = i.split(' ')
			xCoordArray.append(int(separate[0]))
			yCoordArray.append(int(separate[1]))
			#print xCoordArray
			#print yCoordArray
		#print dataArray[:4]
		#print dataArray[4:]
		#for i in range(num_inputs):
			if len(xCoordArray) > 4:
				dataX.append(xCoordArray[:4])
				dataY.append(xCoordArray[4:])
				xCoordArray = []
				yCoordArray = []
		
	#os.remove(file_list[0])
else:
	print "No files found"

print "Real Coordinate Data:"
print dataX
print len(dataX)
print dataY
print len(dataY)
print " "
"""
# convert list of lists to array and pad sequences if needed
X = pad_sequences(dataX, maxlen=max_len, dtype='float32')
# reshape X to be [samples, time steps, features]
X = numpy.reshape(X, (X.shape[0], max_len, 1))
# normalize
X = X / float(max_value)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# create and fit the model



#Xmodel = Sequential()
#Xmodel.add(LSTM(32, input_shape=(X.shape[1], 1)))
#Xmodel.add(Dense(y.shape[1], activation='softmax'))

Xmodel = load_model('xModel.h5')

Xmodel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#Xmodel.fit(X, y, epochs=num_epochs, batch_size=batch_size, verbose=2)

#model.load_weights('myWeights.h5')

#summarize performance of the model
#scores = Xmodel.evaluate(X, y, verbose=0)
#print("Model Accuracy: %.2f%%" % (scores[1]*100))
# demonstrate some model predictions
for i in range(num_tests):
	pattern_index = numpy.random.randint(len(dataX))
	pattern = dataX[pattern_index]
	x = pad_sequences([pattern], maxlen=max_len, dtype='float32')
	x = numpy.reshape(x, (1, max_len, 1))
	x = x / float(max_value)
	prediction = Xmodel.predict(x, verbose=0)
	index = numpy.argmax(prediction)
	result = index
	seq_in = [value for value in pattern]
	print seq_in, "->", result
#Xmodel.save('LearningModelPresentation3.h5')
Xmodel.save_weights('PresWeights.h5')

