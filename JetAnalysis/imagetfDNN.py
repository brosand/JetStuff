
#http://machinelearningmastery.com/object-recognition-convolutional-neural-networks-keras-deep-learning-library/
# Plot ad hoc CIFAR10 instances
from keras.datasets import cifar10

# Simple CNN model for CIFAR-10
import numpy
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

K.set_image_dim_ordering('th')
    
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)


# load data
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# Pixesl are RGB so range from 0 - 255
# normalize inputs from 0-255 to 0.0-1.0
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0

#We can use a one hot encoding to transform them into a binary matrix in order to best model the classification problem. We know there are 10 classes for this problem, so we can expect the binary matrix to have a width of 10.   
# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

#Lets design a deep version of the simple CNN above. We can introduce an additional round of convolutions with many more feature maps. We will use the same pattern of Convolutional, Dropout, Convolutional and Max Pooling layers.

#This pattern will be repeated 3 times with 32, 64, and 128 feature maps. The effect be an increasing number of feature maps with a smaller and smaller size given the max pooling layers. Finally an additional and larger Dense layer will be used at the output end of the network in an attempt to better translate the large number feature maps to class values.

#We can summarize a new network architecture as follows:

#    Convolutional input layer, 32 feature maps with a size of 3x3 and a rectifier activation function.
#   Dropout layer at 20%.
#    Convolutional layer, 32 feature maps with a size of 3x3 and a rectifier activation function.
#    Max Pool layer with size 2x2.
#    Convolutional layer, 64 feature maps with a size of 3x3 and a rectifier activation function.
#    Dropout layer at 20%.
#    Convolutional layer, 64 feature maps with a size of 3x3 and a rectifier activation function.
#    Max Pool layer with size 2x2.
#    Convolutional layer, 128 feature maps with a size of 3x3 and a rectifier activation function.
#    Dropout layer at 20%.
#    Convolutional layer,128 feature maps with a size of 3x3 and a rectifier activation function.
#    Max Pool layer with size 2x2.
#    Flatten layer.
#    Dropout layer at 20%.
#    Fully connected layer with 1024 units and a rectifier activation function.
#    Dropout layer at 20%.
#    Fully connected layer with 512 units and a rectifier activation function.
#    Dropout layer at 20%.
#    Fully connected output layer with 10 units and a softmax activation function.


# Create the model
model = Sequential()
model.add(Conv2D(40, (3, 3), input_shape=(3, 32, 32), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(Conv2D(40, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))
# Compile model
epochs = 25
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())


#We can fit this model with 25 epochs and a batch size of 64 9not clear why different but ok.

#A small number of epochs was chosen to help keep this tutorial moving. Normally the number of epochs would be one or two orders of magnitude larger for this problem.

#Once the model is fit, we evaluate it on the test dataset and print out the classification accuracy.
    
# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
