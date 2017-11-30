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

Class Brain: 
    
    def runBrain(self):
    # fix random seed for reproducibility
    numpy.random.seed()
    # prepare the dataset of input to output pairs 
    num_inputs = 10
    num_tests = 10
    max_len = 5
    min_seq_len = 2
    max_seq_len = 8
    max_value = 50
    max_velocity = 2
    max_velocity = 2
    max_velocity = 2
    batch_size = 1
    num_epochs = 1
    xCoordArray = []
    yCoordArray = []
    x2CoordArray = []
    y2CoordArray = []
    dataX = []
    dataY = []
    dataX2 = []
    dataY2 = []
    fileCount = 0

    file_list = glob.glob('PSP*')

    file_list.sort()
    #print "\n".join(file_list)
    if len(file_list) > 0:
        fileCount = 0
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
                    dataX2.append(yCoordArray[:4])
                    dataY2.append(yCoordArray[4:])
                    xCoordArray = []
                    yCoordArray = []
                    x2CoordArray = []
                    y2CoordArray = []
        
            os.remove(file_list[fileCount])
            fileCount += 1
    else:
        print "No files found"
    #print dataX
    #print dataY

    # convert list of lists to array and pad sequences if needed
    X = pad_sequences(dataX, maxlen=max_len, dtype='float32')
    # reshape X to be [samples, time steps, features]
    X = numpy.reshape(X, (X.shape[0], max_len, 1))
    # normalize
    X = X / float(max_value)
    # one hot encode the output variable
    y = np_utils.to_categorical(dataY)
    # load the model

    Xmodel = load_model('xModel.h5')


    Xmodel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    Ymodel = load_model('yModel.h5')

    Ymodel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # demonstrate some model predictions


    for i in range(len(dataX)):
        pattern = dataX[i]
        pattern2 = dataX2[i]
        x = pad_sequences([pattern], maxlen=max_len, dtype='float32')
        x2 = pad_sequences([pattern2], maxlen=max_len, dtype='float32')
        #print x
        x = numpy.reshape(x, (1, max_len, 1))
        x = x / float(max_value)
        x2 = numpy.reshape(x2, (1, max_len, 1))
        x2 = x2 / float(max_value)
        #print x
        prediction = Xmodel.predict(x, verbose=0)
        prediction2 = Ymodel.predict(x2, verbose=0)
        #print prediction
        index = numpy.argmax(prediction)
        index2 = numpy.argmax(prediction2)
        #print index
        result = index
        result2 = index2
        seq_in = [value for value in pattern]
        seq_in2 = [value for value in pattern2]
        if abs(result - dataY[i]) < 2:
            verdict = "normal"
        else:
            verdict = "ABNORMAL"
        if abs(result2 - dataY2[i]) < 2:
            verdict2 = "normal"
        else: 
            verdict2 = "ABNORMAL"	
        print "File", i+1
        print 'X:', seq_in, "->", result, dataY[i], verdict
        print 'Y:', seq_in2, "->", result2, dataY2[i], verdict2
        print ''


