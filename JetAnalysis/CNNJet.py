import numpy as np
import pandas
import keras
import math
import sys

from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras import backend as K

K.set_image_dim_ordering('th')



batch_size = 32 # in each iteration, we consider 32 training examples at once
nEpochs = 5 # we iterate 200 times over the entire training set
kernal_size = 3 # we will use 3x3 kernels throughout
pool_size = 2 # we will use 2x2 pooling throughout
conv_depth_1 = 32 # we will initially have 32 kernels per conv. layer...
conv_depth_2 = 64 # ...switching to 64 after the first pooling layer
drop_prob_1 = 0.25 # dropout after pooling with probability 0.25
drop_prob_2 = 0.5 # dropout in the FC layer with probability 0.5
hidden_size = 512 # the FC layer will have 512 neurons
numClasses = 2 # the number of possible outputs
nLayers = 2
nNodes = 0
inputDim = 0
nLayers1 = 2
nLayers2 = 2
verboseL = 0
#DRAW OUT SCHEMATIC


# def saveModel():

# def baselineModel(X_train, dimension):
    # model.add(Conv2D(40, (3, 3), input_shape=(1, 3, 3), activation='relu', padding='same'))
    # model.add(Dropout(0.2))
    # model.add(Conv2D(40, (3, 3), activation='relu', padding='same'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
#GO THROUGH HERE AND NN, SIMPLIFY THE LIST OF VARIABLES SO LESS UGLY IFS AND FOR
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
    for file in range(numFiles):
        inputFiles.append('preTxt/' + sys.argv[file + 2])
    for a in range(len(sys.argv)):
        if (sys.argv[a] == 'nEpochs'):
            nEpochs = int(sys.argv[a+1])
        if (sys.argv[a] == 'inputDim'):
            inputDim = int(math.pow(float(sys.argv[a+1]),2))
        if (sys.argv[a] == 'numClasses'):
            numClasses = int(sys.argv[a+1])
        if (sys.argv[a] == 'batch_size'):
            batch_size = int(sys.argv[a+1])
        if (sys.argv[a] == 'kernal_size'):
            kernal_size = int(math.pow(float(sys.argv[a+1]),2))
        if (sys.argv[a] == 'pool_size'):
            pool_size = int(sys.argv[a+1])
        if (sys.argv[a] == 'conv_depth_1'):
            conv_depth_1 = int(sys.argv[a+1])


        if (sys.argv[a] == 'conv_depth_2'):
            conv_depth_2 = int(math.pow(float(sys.argv[a+1]),2))
        if (sys.argv[a] == 'drop_prob_1'):
            drop_prob_1 = int(sys.argv[a+1])
        if (sys.argv[a] == 'drop_prob_2'):
            drop_prob_2 = int(sys.argv[a+1])
        if (sys.argv[a] == 'hidden_size'):
            hidden_size = int(sys.argv[a+1])
        if (sys.argv[a] == 'verbose'):
            verboseL = int(sys.argv[a+1])


def saveInfo(inputFiles, nEpochs, accuracy, nOutputNodes):
    output=open('NeuralNetData.txt', 'a')
    output.write('CNN   ')
    for i, file in enumerate(inputFiles):
        output.write('File %i: %s   ' % (i+1, file))

    output.write('Number of epochs: %i   ' % nEpochs)
    output.write('Number of Output Nodes: %s   ' % nOutputNodes)
    output.write("Image dimension: %i" %inputDim)
    output.write("Accuracy on test sample: %.2f%% " % accuracy)
    output.write("Number of convolutional layers with depth %i: %i " %(conv_depth_1, nLayers1))
    output.write("Number of convolutional layers with depth %i: %i \n" %(conv_depth_2, nLayers2))

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
    X = X.reshape(X.shape[0], 1, dimension, dimension)

    encoder = LabelEncoder()
    encoder.fit(Y)
    encoded_Y = encoder.transform(Y)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)

    # split data into a training and test sample
    validation_size = 0.20
    X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_y, test_size=validation_size, random_state=seed)
    # X = X.reshape(X.shape[0], dimension, dimension, 1)
    # print(X_train.shape)
    # print(X_train.shape[0])
    # print(X_train.shape[1])
    # print(X_train.shape[1:])


    numClasses = Y_test.shape[1]
    model = Sequential()

    model.add(Conv2D(conv_depth_1, (kernal_size, kernal_size), input_shape=(X_train.shape[1:]), activation='relu', padding='same'))
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




    #We can fit this model with 25 epochs and a batch size of 64 9not clear why different but ok.

    #A small number of epochs was chosen to help keep this tutorial moving. Normally the number of epochs would be one or two orders of magnitude larger for this problem.

    #Once the model is fit, we evaluate it on the test dataset and print out the classification accuracy.
        
    # Fit the model
    print X_train.shape
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=nEpochs, batch_size=batch_size, verbose=verboseL)
    # Final evaluation of the model
    scores = model.evaluate(X_test, Y_test, verbose=1)
    print("\n(FOR JUST THE TEST SET) %s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    model.save('CNNModel')

    saveInfo(inputFiles, nEpochs, scores[1]*100, numClasses)
# def testModel(model):

if __name__ == '__main__':
    trainModel()
    # testModel()
