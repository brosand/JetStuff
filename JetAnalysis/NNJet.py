import numpy as np
import pandas
import keras
import math
import csv
import os

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

# from quiver_engine import 
from timeit import default_timer as timer
import sys

nNodes = 1000
inputDim = 5
numClasses = 2
nEpochs = 5
BATCH_SIZE = 5
nLayers = 3
verboseL = 0
networkType = 'DNN'
# define baseline model
#creates a simple fully connected network with one hidden layer that contains 8 neurons.
#The hidden layer uses a rectifier activation function which is a good practice. Because we used a one-hot encoding for our  dataset, the output layer must create 2 output values, one for each class. The output value with the largest value will be taken as the class predicted by the model.

#The network topology of this simple one-layer neural network can be summarized as:

# 8 inputs --> [ 8 hidden nodes ] --> 3 outputs
# Note that we use a "softmax" activation function in tohe output layer. This is to ensure the output values are in the range of 0 and 1 and may be used as predicted probabilities.

# Finally, the network uses the efficient Adam gradient descent optimization algorithm with a logarithmic loss function, which is called "categorical_crossentropy" in Keras.


#make neural net
inputFiles = []
cmdargs = str(sys.argv)
if len(sys.argv) == 1:
    numFiles = int(raw_input("Enter the number of files: "))

    for i in range(numFiles):
        inputFiles.append('preTxt/' + raw_input("Enter file %i: " % (i+1)))
    nEpochs = int(raw_input("Enter the number of epochs: "))
    numClasses = int(raw_input("Enter the number of outputs: "))
    nLayers = int(raw_input("Enter the number of layers: "))
    nNodes = int(raw_input("Enter the number of nodes: "))
    inputDim = int((math.pow(float(raw_input("Enter the dimension (temporary): ")),2)))
else:
    numFiles = int(sys.argv[1])
    numClasses = numFiles
    for file in range(numFiles):
        inputFiles.append('preTxt/' + sys.argv[file + 2])
    for a in range(len(sys.argv)):
        if (sys.argv[a] == 'nEpochs'):
            nEpochs = int(sys.argv[a+1])
        if (sys.argv[a] == 'inputDim'):
            inputDim = int(math.pow(float(sys.argv[a+1]),2))
        if (sys.argv[a] == 'numClasses'):
            numClasses = int(sys.argv[a+1])
        if (sys.argv[a] == 'nNodes'):
            nNodes = int(sys.argv[a+1])
        if (sys.argv[a] == 'nLayers'):
            nLayers = int(sys.argv[a+1])
        if (sys.argv[a] == 'verbose'):
            verboseL = int(sys.argv[a+1])

def saveInfo(inputFiles, nEpochs, sTest, numClasses):
    fieldnames = ['Network Type','inputFile1','inputFile2','inputFile3', 'inputFile4', 'Epochs', 'Image Dimension', 'Accuracy', 'Layers', 'Nodes']
    output = open('NNData.csv', 'a')
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    if os.stat('NNData.csv').st_size==0:
        writer.writeheader()
    for i in range(4):
        if (len(inputFiles) < i):
            inputFiles.append('')
    
    output.writerow({'Network Type': networkType, 'inputFile1': inputFiles[0],'inputFile2': inputFiles[1],
        'inputFile3':inputFiles[2], 'inputFile4': inputFiles[3], 'Epochs': nEpochs,
         'Image Dimension': inputDim, 'Accuracy': sTest, 'Layers': nLayers, 'Nodes': nNodes})

# def baseline_model():
    # create model
    # return model

model = Sequential()
model.add(Dense(nNodes, input_dim=inputDim, activation='relu'))
model.add(Dense(nNodes))
model.add(Dense(nNodes))
model.add(Dense(numClasses, activation='softmax')) #these are the two possible outputs

# Compile model

# fix random seed for reproducibility, later can be time
seed = 7
np.random.seed(seed)

# Open first dataset and read into arrays X,Y, Z

dataset = pandas.read_csv(inputFiles[0],sep=" ",header=None)
array = dataset.values
dimension = array[0, 1]


print("Dimension: %d" % dimension)

X = array[: , 2:int(math.pow(dimension, 2) + 2)]  
Y = array[: , 0]
Z = array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]
# Open second dataset and add information onto end of arrays X,Y, Z
for file in range(1, len(inputFiles)):
    dataset1 = pandas.read_csv(inputFiles[file], sep=" ",header=None)
    array = dataset1.values
    X = np.concatenate((X,array[: , 2:int(math.pow(dimension, 2) + 2)]))
    Y = np.concatenate((Y,array[ : , 0]))
    Z = np.concatenate((Z,array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]))

# encode class values as integers since NN can't work with strings (I think)
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

#print encoded_Y

#There is a KerasClassifier class in Keras that can be used as an Estimator in scikit-learn, the base type of model in the library. The KerasClassifier takes the name of a function as an argument. This function must return the constructed neural network model, ready for training.
#Below is a function that will create a baseline neural network for the iris classification problem.  with buildfn creating the baseline model
# estimator = KerasClassifier(build_fn=model, epochs=nEpochs, batch_size=5, verbose=1)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
   

# split data into a training and test sample
validation_size = 0.20
X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_y, test_size=validation_size, random_state=seed)
# print X_train.shape
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=nEpochs, batch_size=BATCH_SIZE, verbose=verboseL)

# train our NN
# estimator.fit(X_train, Y_train)
#prediction = estimator.predict(X_train)
#print(prediction)

# see how it does on our test data
# predictions = estimator.predict(X_test)
# for i in range(predictions.size):
#     if Y_test[i][predictions[i]] == 1 :
#         print "Got it right"
#     else :
#         print "WRONG!!!!!!!!!!!!!!!!!!!!!!!!!"

#Some more tests for how training is doing
# This takes some time, not sure why

scores = model.evaluate(X_test, Y_test, verbose=1)
print("\n(FOR JUST THE TEST SET) %s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# scores1 = model.evaluate(X, Y, verbose=1)
# print("(FOR WHOLE DATA SET) %s: %.2f%%" % (model.metrics_names[1], scores1[1]*100))

# kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
# print 'finished KFold'

# start = timer()
# results = cross_val_score(estimator, X, dummy_y, cv=kfold)
# end = timer()
# print(end-start)

saveInfo(inputFiles, nEpochs, scores[1]*100, numClasses)
# print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
