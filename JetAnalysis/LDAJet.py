import pandas
import numpy as np
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import metrics as m
from sklearn.utils import shuffle
import ROOT 
import math
import sys

HIST_BOUND = 3

inputs = []
datasets = []
types = []
canvas = ROOT.TCanvas("canvas", "canvas")


nClasses = input("Enter the number of classes among which you would like to discriminate: ")

inputs.append(raw_input("Enter the first txt file: "))
#inputs.append(raw_input("Enter the second txt file: "))

if(nClasses < 2):
    print("Error: you must provide at least 2 classes. Aborting.")
    sys.exit()

# Open first dataset and read into arrays X,Y, Z
datasets.append(pandas.read_csv(inputs[0],sep=" ",header=None))
array = datasets[0].values
dimension = array[0, 1]
print("dimension: %d" % math.pow(dimension, 2))
print("nClasses: %d" % nClasses)
X = array[: , 2:int(math.pow(dimension, 2) + 2)]  
Y = array[: , 0]
types.append(Y[0])
Z = array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]

for i in range (1, nClasses):
    inputs.append(raw_input("Enter file %d: " % int(i+1)))

    # Open next dataset and add information onto end of arrays X,Y, Z
    datasets.append(pandas.read_csv(inputs[i],sep=" ",header=None))
    array = datasets[i].values
    X = np.concatenate((X,array[: , 2:int(math.pow(dimension, 2) + 2)]))
    Y = np.concatenate((Y,array[ : , 0]))
    types.append(array[0][0])
    Z = np.concatenate((Z,array[: , int(math.pow(dimension, 2) + 2):int(math.pow(dimension, 2) + 4)]))

# Randomly split the summed dataset into a training and validation set with 80:20 ratio
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

#look at accuracy of predicitons
for i in range(Y_validation.size):
    if predictions[i] == Y_validation[i] :
        print "Got it right! Entry", i, predictions[i],Y_validation[i]
    else:
        print "Got it wrong", predictions[i],Y_validation[i]

#put all print statements after the loop
# print("X_trans[0][0]")
# print(X_trans[0][0])

# print("X_trans[1][0]")
# print(X_trans[1][0])

# print("X_trans[2][0]")
# print(X_trans[2][0])

# #this one gives error
# #print("X_trans[0][1]")
# #print(X_trans[0][1])

# print("X_trans[0]")
# print(X_trans[0])

# print("X_trans[1]")
# print(X_trans[1])

# print("X_trans[2]")
# print(X_trans[2])

print("size of X_trans: ")
print(X_trans.size)




print("lda coef thing: ")
print(lda.coef_)
print("coef_ size: ")
print(lda.coef_.size)

if (nClasses == 2):

    histogram1 = ROOT.TH1F("histogram1", "histogram1", 1000, -HIST_BOUND, HIST_BOUND)
    histogram2 = ROOT.TH1F("histogram2", "histogram2", 1000, -HIST_BOUND, HIST_BOUND)
    histogram1.GetXaxis().SetTitle("X_trans[j]");
    histogram1.GetYaxis().SetTitle("frequency");

    for j in range(X_trans.size):

        if(Y_train[j]  == types[0]):

            histogram1.Fill(X_trans[j][0])

        elif(Y_train[j] == types[1]):

            histogram2.Fill(X_trans[j][0])

# h1->Draw();
# h1->SetLineColor(kRed);
# h2->Draw("same");
# h2->SetLineColor(kBlue);
# c1->Update();

    title = types[0]+ "-" + types[1]

    canvas.cd()
    histogram1.Draw()
    histogram1.SetTitle(title)
    histogram2.Draw("same")
    histogram2.SetLineColor(2) #red
    canvas.SaveAs(title + ".pdf")

# if(nClasses == 3):
#     histogram1 = ROOT.TH2F("histogram1", "histogram1", 1000, -HIST_BOUND, HIST_BOUND, 1000, -HIST_BOUND, HIST_BOUND)
#     histogram2 = ROOT.TH2F("histogram2", "histogram2", 1000, -HIST_BOUND, HIST_BOUND, 1000, -HIST_BOUND, HIST_BOUND)
#     histogram3 = ROOT.TH2F("histogram3", "histogram3", 1000, -HIST_BOUND, HIST_BOUND, 1000, -HIST_BOUND, HIST_BOUND)

#     histogram1.GetZaxis().SetTitle("frequency");

#     print(X_trans.size)

#     # for j in range(X_trans.size):

#     for j in range(X_trans.size):

#         # if(Y_train[j]  == types[0]):

#         histogram1.Fill(X_trans[j][0], X_trans[j][1])

#         # elif(Y_train[j] == types[1]):

#             # histogram2.Fill(X_trans[j][0], X_trans[j][1])

#         # elif(Y_train[j] == types[2]):

#             # histogram3.Fill(X_trans[j][0], X_trans[j][1])

#     title = types[0]+ "-" + types[1] + "-" + types[2]
#     canvas.cd()
#     histogram1.Draw("lego")
#     histogram1.SetTitle(title)
#     histogram2.Draw("same")
#     histogram2.SetLineColor(2) #red
#     histogram3.Draw("same")
#     histogram3.SetLineColor(3) #green
#     canvas.SaveAs(title + ".pdf")



print(m.accuracy_score(Y_validation, predictions))
#print(m.confusion_matrix(Y_validation, predictions))
#print(m.classification_report(Y_validation, predictions))



