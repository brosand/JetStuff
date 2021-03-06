import numpy as np
import pandas
import keras
import math
import sys
import csv
import os
import time
import argparse


from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras import backend as K
from keras.utils import plot_model
#from quiver_engine import server

K.set_image_dim_ordering('tf')



nLayers = 2
nLayers1 = 2
nLayers2 = 2
networkType = 'CNN'
quiver = 0
#DRAW OUT SCHEMATIC

parser=argparse.ArgumentParser()
parser.add_argument('--data', action='append', nargs='+',  help="datasets to be tested on")
parser.add_argument('--validation_size', default=.2, help="fraction of sample to be saved for evaluation", type=float)
parser.add_argument('--epochs', default=3, help="number of jets", type=int)
parser.add_argument('--batch_size', default=32, help="number of jets", type=int)
parser.add_argument('--kernal_size', default=5, help="number of jets", type=int)
parser.add_argument('--pool_size', default=2, help="number of jets", type=int)
parser.add_argument('--conv_depth_1', default=32, help="number of jets", type=int)
parser.add_argument('--conv_depth_2', default=64, help="number of jets", type=int)
parser.add_argument('--drop_prob_1', default=.25, help="number of jets", type=float)
parser.add_argument('--drop_prob_2', default=.5, help="number of jets", type=float)
parser.add_argument('--hidden_size', default=512, help="number of jets", type=int)
parser.add_argument('--verbose', default=1, help="verbose logging", type=int)
parser.add_argument('--classes', default='', help="classes to compare")
parser
args = parser.parse_args()

validation_size=args.validation_size
nEpochs=args.epochs
batch_size=args.batch_size
kernal_size=args.kernal_size
pool_size=args.pool_size
conv_depth_1=args.conv_depth_1
conv_depth_2=args.conv_depth_2
drop_prob_1=args.drop_prob_1
drop_prob_2=args.drop_prob_2
hidden_size=args.hidden_size

inputFiles = []
for i in args.data:
    inputFiles.append(i[0])
classes=args.classes
numClasses=len(inputFiles)
if (numClasses < 2):
    raise Exception('Not enough classes to train on')

def saveInfo(dimension, inputFiles, nEpochs, accuracy, nOutputNodes):
    fieldnames = ['Date', 'Time', 'Network Type','inputFile1','inputFile2','inputFile3', 'inputFile4', 'Epochs', 'Image Dimension', 'Accuracy', 'Layers', 'Nodes', 'Kernal size']
    output = open('NNData.csv', 'a')
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    if os.stat('NNData.csv').st_size==0:
        writer.writeheader()
    for i in range(5):
        if (len(inputFiles) < i):
            inputFiles.append('')
    
    writer.writerow({'Date': (time.strftime("%d/%m/%Y")),'Time': (time.strftime("%H:%M:%S")), 'Network Type': networkType, 'inputFile1': inputFiles[0],'inputFile2': inputFiles[1],
        'inputFile3':inputFiles[2], 'inputFile4': inputFiles[3], 'Epochs': nEpochs,
         'Image Dimension': int(math.pow(dimension,2)), 'Accuracy': accuracy, 'Layers': (nLayers1+nLayers2), 'Nodes': nNodes, 
         'Kernal size': kernal_size})

def trainModel():

    # fix random seed for reproducibility, later can be time
    seed = 7
    np.random.seed(seed)

    # numFiles = int(raw_input("Enter the number of files: "))

    # inputFiles = []
    # for i in range(numFiles):
    #     inputFiles.append(raw_input("Enter file %i: " % (i+1)))

    # nEpochs = int(raw_input("Enter the number of epochs: "))
    # nOutputNodes = int(raw_input("Enter the number of outputs: "))
    # nLayers = int(raw_input("Enter the number of layers: "))
    dataset = pandas.read_csv(inputFiles[0],sep=" ",header=None)
    array = dataset.values
    dimension = array[0, 1]

    print("Dimension: %d" % math.pow(dimension, 2))
    #Does the array inside x need to be an np.array? or a normal array
    X = array[: , 2: int(math.pow(dimension, 2) + 2)]
    Y = array[: , 0]
    Z = array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]
    # Open second dataset and add information onto end of arrays X,Y, Z
    for file in range(1, len(inputFiles)):
        dataset1 = pandas.read_csv(inputFiles[file], sep=" ",header=None)
        array = dataset1.values
        X = np.concatenate((X,array[: , 2:int(math.pow(dimension, 2) + 2)]))
        Y = np.concatenate((Y,array[ : , 0]))
        Z = np.concatenate((Z,array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]))
    #DOUBLE CHECK THAT RIGHT ORDER
    X = X.reshape(X.shape[0], dimension, dimension, 1)

    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)

    # split data into a training and test sample
    validation_size = 0.10
    Q=np.zeros((X.shape[0],X.shape[1],X.shape[2],2))
    X = np.concatenate((Q,X),3)
    # print X.shape
    X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_y, test_size=validation_size, random_state=seed)
    # print X_train.shape
    # print X_train.shape[1:]
    # X = X.reshape(X.shape[0], dimension, dimension, 1)
    # print(X_train.shape)
    # print(X_train.shape[0])
    # print(X_train.shape[1])
    # print(X_train.shape[1:])


    numClasses = Y_test.shape[1]
    model = Sequential()

    model.add(Conv2D(conv_depth_1,(kernal_size, kernal_size), input_shape=(X_train.shape[1:]), activation='relu', padding='same'))
    model.add(Dropout(drop_prob_1))
    model.add(Conv2D(conv_depth_1, (kernal_size, kernal_size), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))
    model.add(Conv2D(conv_depth_2, (kernal_size, kernal_size), activation='relu', padding='same'))
    model.add(Dropout(drop_prob_2))
    model.add(Conv2D(conv_depth_2, (kernal_size, kernal_size), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))

    model.add(Flatten())
    model.add(Dense(hidden_size, activation='relu'))
    model.add(Dropout(drop_prob_2))
    model.add(Dense(numClasses, activation='softmax'))
    # model = baselineModel(X_train, dimension)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.fit(X_train, Y_train, batch_size=batch_size, epochs=NUM_EPOCHS, verbose=1)




    #We can fit this model with 25 epochs and a batch size of 64 9 not clear why different but ok.

    #Once the model is fit, we evaluate it on the test dataset and print out the classification accuracy.
    # Fit the model
    plot_model(model, to_file='model.png')
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=nEpochs, batch_size=batch_size, verbose=args.verbose)
    # Final evaluation of the model
    scores = model.evaluate(X_test, Y_test, verbose=1)
    print("\nTest set accuracy %s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    model.save('CNNModel%s.h5' % (time.strftime("%H:%M:%S")))
     # if (quiver==1):
    # server.launch(model, [1,['a','b']])

    saveInfo(dimension, inputFiles, nEpochs, scores[1]*100, numClasses)
# def testModel(model):

if __name__ == '__main__':
    # parse = argparse.ArgumentParser()

    #  parser.add_argument(
    #   '--nEpochs',
    #   type=int,
    #   default=5,
    #   help='Number of epochs for neural network to run.'
    #   )
    # FLAGS, unparsed = parser.parse_known_args()
    trainModel()
    # testModel()
