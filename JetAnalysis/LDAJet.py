import pandas
import numpy as np
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import metrics as m
from sklearn.utils import shuffle
from ROOT import gROOT, TCanvas, TH2D
import math

input1 = raw_input("Enter the first txt file: ")
input2 = raw_input("Enter the second txt file: ")

# Open first dataset and read into arrays X,Y, Z
dataset = pandas.read_csv(input1,sep=" ",header=None)
array = dataset.values
dimension = array[0, 1]
print("dimension: %d" % math.pow(dimension, 2))
X = array[: , 2:int(math.pow(dimension, 2) + 2)]  
Y = array[: , 0]
Z = array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]

#print(X)
#print(Y)


# Open second dataset and add information onto end of arrays X,Y, Z

dataset2 = pandas.read_csv(input2,sep=" ",header=None)
array = dataset2.values
X = np.concatenate((X,array[: , 2:int(math.pow(dimension, 2) + 2)]))
Y = np.concatenate((Y,array[ : , 0]))
Z = np.concatenate((Z,array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]))

# print(Y)
# print(X)

# Randonly split the summed dataset into a training and validation set with 80:20 ratio
validation_size = 0.15
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

# print(X_train)
# print Y_train 

# Run LDA

lda = LinearDiscriminantAnalysis()
lda.fit(X_train, Y_train)
# lda.fit(zip(*(shuffle(X_train, Y_train))))


# project training data onto found axes so can look later at plots of how its discriminating
X_trans = lda.transform(X_train)
# Transform validation set  onro these new axes
X_trans2 = lda.transform(X_validation)

#Make predictions as to what each data row is in the validation set
predictions = lda.predict(X_validation)

#lda.coef_

#look at accuracy of predicitons
for i in range(Y_validation.size):
    if predictions[i] == Y_validation[i] :
        print "Got it right! Entry", i, predictions[i],Y_validation[i]
    else:
        print "Got it wrong", predictions[i],Y_validation[i]

print(m.accuracy_score(Y_validation, predictions))
print(m.confusion_matrix(Y_validation, predictions))
print(m.classification_report(Y_validation, predictions))



