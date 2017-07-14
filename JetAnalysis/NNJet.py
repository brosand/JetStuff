import numpy as np
import pandas
import keras
import math

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

N_NODES = 25
N_OUTPUT_NODES = 4
# define baseline model
#creates a simple fully connected network with one hidden layer that contains 8 neurons.
#The hidden layer uses a rectifier activation function which is a good practice. Because we used a one-hot encoding for our  dataset, the output layer must create 2 output values, one for each class. The output value with the largest value will be taken as the class predicted by the model.

#The network topology of this simple one-layer neural network can be summarized as:

# 8 inputs --> [ 8 hidden nodes ] --> 3 outputs
# Note that we use a "softmax" activation function in tohe output layer. This is to ensure the output values are in the range of 0 and 1 and may be used as predicted probabilities.

# Finally, the network uses the efficient Adam gradient descent optimization algorithm with a logarithmic loss function, which is called "categorical_crossentropy" in Keras.


#make neural net

input1 = raw_input("Enter the first txt file: ")
input2 = raw_input("Enter the second txt file: ")
input3 = raw_input("Enter the third txt file: ")
input4 = raw_input("Enter the fourth txt file: ")
inputDim = int(raw_input("Enter the Jet Dimension: "))
nEpochs = int(raw_input("Enter the number of epochs: "))

def saveInfo(input1, input2, nEpochs, mean, std):
    output=open('NeuralNetData.txt \n', 'a')
    output.write('Tree 1: %s \n' % input1)
    output.write('Tree 2: %s \n' % input2)
    output.write('Tree 3: %s \n' % input3)
    output.write('Tree 4: %s \n' % input4)

    output.write('Number of epochs: %i \n' % nEpochs)
    output.write('Number of Nodes: %s \n' % N_NODES)
    output.write('Number of Output Nodes: %s \n' % N_OUTPUT_NODES)
    output.write("Baseline: %.2f%% (%.2f%%) \n" % (mean, std))

def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(N_NODES, input_dim=inputDim, activation='relu'))
    model.add(Dense(N_NODES))
    model.add(Dense(N_NODES))
    model.add(Dense(N_OUTPUT_NODES, activation='softmax')) #these are the two possible outputs

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model




# fix random seed for reproducibility, later can be time
seed = 7
np.random.seed(seed)

# Open first dataset and read into arrays X,Y, Z

dataset = pandas.read_csv(input1,sep=" ",header=None)
array = dataset.values
dimension = array[0, 1]
X = array[: , 2:int(math.pow(dimension, 2) + 2)]  
Y = array[: , 0]
Z = array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]

# Open second dataset and add information onto end of arrays X,Y, Z

dataset2 = pandas.read_csv(input2, sep=" ",header=None)
array = dataset2.values
dimension = array[0, 1]
X = np.concatenate((X,array[: , 2:int(math.pow(dimension, 2) + 2)]))
Y = np.concatenate((Y,array[ : , 0]))
Z = np.concatenate((Z,array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]))

# Open third dataset and read into arrays X,Y, Z

dataset3 = pandas.read_csv(input3,sep=" ",header=None)
array = dataset3.values
dimension = array[0, 1]
X = np.concatenate((X,array[: , 2:int(math.pow(dimension, 2) + 2)]  ))
Y = np.concatenate((Y,array[: , 0]))
Z = np.concatenate((Z,array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]))

# Open fourth dataset and add information onto end of arrays X,Y, Z

dataset4 = pandas.read_csv(input4, sep=" ",header=None)
array = dataset4.values
dimension = array[0, 1]
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

estimator = KerasClassifier(build_fn=baseline_model, epochs=nEpochs, batch_size=5, verbose=1)

# split data into a training and test sample
validation_size = 0.20
X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_y, test_size=validation_size, random_state=seed)


# train our NN
estimator.fit(X_train, Y_train)
#prediction = estimator.predict(X_train)
#print(prediction)

# see how it does on our test data
predictions = estimator.predict(X_test)
for i in range(predictions.size):
    if Y_test[i][predictions[i]] == 1 :
        print "Got it right"
    else :
        print "WRONG!!!!!!!!!!!!!!!!!!!!!!!!!"

#Some more tests for how training is doing
# This takes some time, not sure why
kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
print 'finished KFold'
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
saveInfo(input1, input2, nEpochs, results.mean()*100, results.std()*100)
