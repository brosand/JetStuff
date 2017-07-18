import numpy as np
import pandas
import keras
import math

from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras import backend as K

K.set_image_dim_ordering('th')



BATCH_SIZE = 32 # in each iteration, we consider 32 training examples at once
NUM_EPOCHS = 5 # we iterate 200 times over the entire training set
KERNEL_SIZE = 3 # we will use 3x3 kernels throughout
POOL_SIZE = 2 # we will use 2x2 pooling throughout
CONV_DEPTH_1 = 32 # we will initially have 32 kernels per conv. layer...
CONV_DEPTH_2 = 64 # ...switching to 64 after the first pooling layer
DROP_PROB_1 = 0.25 # dropout after pooling with probability 0.25
DROP_PROB_2 = 0.5 # dropout in the FC layer with probability 0.5
HIDDEN_SIZE = 512 # the FC layer will have 512 neurons
NUM_CLASSES = 2 # the number of possible outputs
inputFiles = ['aJetPre.txt', 'cJetPre.txt']
nOutputNodes = 2



# def saveModel():

# def baselineModel(X_train, dimension):
    # model.add(Conv2D(40, (3, 3), input_shape=(1, 3, 3), activation='relu', padding='same'))
    # model.add(Dropout(0.2))
    # model.add(Conv2D(40, (3, 3), activation='relu', padding='same'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))


def saveInfo(inputFiles, nEpochs, accuracy, nOutputNodes):
    output=open('NeuralNetData.txt', 'a')
    output.write('CNN   ')
    for i, file in enumerate(inputFiles):
        output.write('File %i: %s   ' % (i+1, file))

    output.write('Number of epochs: %i   ' % nEpochs)
    output.write('Number of Output Nodes: %s   ' % nOutputNodes)
    output.write("App accuracy: %f \n\n" % accuracy)

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

    NUM_CLASSES = Y_test.shape[1]
    model = Sequential()

    model.add(Conv2D(40, (3, 3), input_shape=(1, dimension, dimension), activation='relu', padding='same'))
    model.add(Dropout(0.2))
    model.add(Conv2D(40, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(Dropout(0.2))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(DROP_PROB_2))
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    # model = baselineModel(X_train, dimension)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # model.fit(X_train, Y_train, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS, verbose=1)




    #We can fit this model with 25 epochs and a batch size of 64 9not clear why different but ok.

    #A small number of epochs was chosen to help keep this tutorial moving. Normally the number of epochs would be one or two orders of magnitude larger for this problem.

    #Once the model is fit, we evaluate it on the test dataset and print out the classification accuracy.
        
    # Fit the model
    print X_train.shape
    model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=NUM_EPOCHS, batch_size=BATCH_SIZE, verbose=1)
    # Final evaluation of the model
    scores = model.evaluate(X_test, Y_test, verbose=1)
    accuracy = (scores[1]*100)
    print accuracy
    model.save('CNNModel')

    saveInfo(inputFiles, NUM_EPOCHS, accuracy, nOutputNodes)
# def testModel(model):

if __name__ == '__main__':
    trainModel()
    # testModel()