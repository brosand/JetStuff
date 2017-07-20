import pandas
import numpy as np
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import metrics as m
from sklearn.utils import shuffle
import ROOT 
import math
import sys
import csv
import os
import time
# from sklearn.decomposition import PCA

HIST_BOUND = 3

def saveInfo(nClasses, inputs, dimension, score):
    fieldnames = ['Date','Time','Number of Classes','inputfile1', 'inputfile2' , 'inputfile3', 'inputfile4', 'dimension', 'score', 'Cone R']
    print(fieldnames)
    for i in range(5):
        if (len(inputs) < i):
            inputs.append('')

    output = open('LDA_Data.csv', 'a')
    writer = csv.DictWriter(output, fieldnames = fieldnames)

    if (os.stat('LDA_Data.csv').st_size==0):
        writer.writeheader()
        print("Inside if")
    else:
        print("inside else")
        most_recent_heading_row_number = 0 #get rid
        with open('LDA_Data.csv', 'r') as original:
            for iLine, line in enumerate(original): #get rid enum
                print(line)
                print("line split 0: %s" % line.split(',')[0])
                if (line.split(',')[0] == 'Date'):
                    most_recent_heading_row_number = iLine #get rid
                    most_recent_heading = line

        print("most_recent_heading_row_number: %d" % most_recent_heading_row_number)
        print(most_recent_heading.rstrip().split(','))
        if(most_recent_heading.rstrip().split(',') != fieldnames):
            writer.writeheader()
    
    writer.writerow({'Date': time.strftime("%d/%m/%Y"), 'Time': time.strftime("%H:%M:%S"),'Number of Classes': nClasses, 'inputfile1':inputs[0], 'inputfile2':inputs[1], 'inputfile3':inputs[2], 'inputfile4':inputs[3], 'dimension':dimension, 'score':score, 'Cone R':0.6})



inputs = []
cmdargs = str(sys.argv)
datasets = []
types = []
canvas = ROOT.TCanvas("canvas", "canvas")
canvas2 = ROOT.TCanvas("canvas2", "canvas2")

if (len(sys.argv) == 1):
    nClasses = input("Enter the number of classes among which you would like to discriminate: ")
    if(nClasses < 2):
        print("Error: you must provide at least 2 classes. Aborting.")
        sys.exit()
    for i in range(nClasses):
        inputs.append(raw_input("Enter file %d: " % int(i+1)))

else:
    nClasses = 0
    for a in range(len(sys.argv)):
        if ('.txt' in sys.argv[a]):
            inputs.append(sys.argv[a])
            nClasses+=1


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

# print("n_components size: %d" % X_train.size)
# print("n_components len: %d" % len(X_train))
# print("n_components index 0: %d" % len(X_train[0]))

# pca = PCA(n_components = (len(X_train)-2))
# pca.fit(X_train)
# X_train = pca.transform(X_train)

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

    histogram1 = ROOT.TH1F("histogram1", "histogram1", 200, -HIST_BOUND, HIST_BOUND)
    histogram2 = ROOT.TH1F("histogram2", "histogram2", 200, -HIST_BOUND, HIST_BOUND)
    histogramCOEF = ROOT.TH2F("histogramCOEF", "histogramCOEF", dimension, 0, dimension, dimension, 0, dimension)
    histogram1.GetXaxis().SetTitle("X_trans[j]");
    histogram1.GetYaxis().SetTitle("frequency");

#how many times was each type guessed?
#predictions and y validation
    denom1 = 0
    denom2 = 0 #turn to array
    num1 = 0
    num2 = 0
    for i in range(Y_validation.size):
        if(Y_validation[i] == types[0]):
            denom1 +=1

        elif(Y_validation[i] == types[1]):
            denom2 +=1

        if(predictions[i] == types[0]):
            num1 +=1

        elif(predictions[i] == types[1]):
            num2 +=1

    efficiency1 = num1/float(denom1)
    efficiency2 = num2/float(denom2)

    print("Efficiency for %s: %f" % (types[0], efficiency1))
    print("Efficiency for %s: %f" % (types[1], efficiency2))

    hits1 = 0
    hits2 = 0
    for j in range(X_trans.size):

        if(Y_train[j]  == types[0]):

            hits1 += 1

        elif(Y_train[j] == types[1]):

            hits2 += 1

    for j in range(X_trans.size):

        if(Y_train[j]  == types[0]):
            #histogram1.Scale(1/hits1)
            histogram1.Fill(X_trans[j][0], 1/float(hits1))

        elif(Y_train[j] == types[1]):
            #histogram2.Scale(1/hits2)
            histogram2.Fill(X_trans[j][0], 1/float(hits2))

    title = types[0]+ "-" + types[1]

    canvas.cd()
    histogram1.Draw()
    histogram1.SetTitle(title)
    histogram2.Draw("same")
    histogram2.SetLineColor(2) #red
    canvas.SaveAs(title + ".pdf")


    #fill histcoef
    print("lda coef 0, 0 = %f" % lda.coef_[0][0])
    print("lda coef 0, 1 = %f" % lda.coef_[0][1])

    counter = 0
    for column in range(dimension): #not sold on order of filling
        for row in range (dimension):
            #histogramCOEF.Fill(row, column, pca.inverse_transform(lda.coef_[0][counter]))
            histogramCOEF.Fill(column, row, lda.coef_[0][counter])

            counter += 1

    canvas2.cd()
    histogramCOEF.Draw("LEGO2Z")
    histogramCOEF.SetTitle(title + " LDA Coef")
    histogramCOEF.GetXaxis().SetTitle("column");
    histogramCOEF.GetYaxis().SetTitle("row");
    histogramCOEF.GetZaxis().SetTitle("LDA Coef of that pixel");
    canvas2.SaveAs(title + "LDACoef.pdf")

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


score = m.accuracy_score(Y_validation, predictions)

print(score)
#print(m.confusion_matrix(Y_validation, predictions))
#print(m.classification_report(Y_validation, predictions))

saveInfo(nClasses, inputs, dimension, score)


