from __future__ import print_function
import PIL
import numpy as np
import pandas
import math
import argparse
import json
import ROOT
import sys

from PIL import Image
from scipy.misc import imsave
import numpy as np
import time
from keras import backend as K
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from keras.models import model_from_json
from keras.utils import np_utils
from sklearn.preprocessing import normalize

HIST_BOUND_CONE = 1.0
NUM_CLASSES = 2
# from keras.model import predict
parser = argparse.ArgumentParser()
parser.add_argument('--data', default='r1.0/A21.txt', help="dataset to be tested on")
parser.add_argument('--weights', default='waNNModels/ABweights.h5' , help="weights of model")
parser.add_argument('--architecture', default='waNNModels/ABmodel.json' , help="architecture of model")
parser.add_argument('--validation_size', default=10000, help="number of jets", type=int)
parser.add_argument('--classes', default='', help="classes of data")
parser.add_argument('--notes', default='', help="notes")

args = parser.parse_args()
if (args.classes==''):
    args.classes=raw_input('Enter classes: ')

dataset = pandas.read_csv(args.data ,sep=" ",header=None)
array = dataset.values
dimension = (array[0, 1])

histPearson = ROOT.TH2F("histPearson", "Pearson Coefficient Histogram", dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE, dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE)

X = array[: , 2:(dimension*dimension) + 2]  

X = X[:args.validation_size]
P = np.zeros((args.validation_size))


json_file = open(args.architecture, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(args.weights)
print('Number of test cases, dimension: ' + str(X.shape))

sumP = 0
sumI = np.zeros((dimension*dimension))

# term = TerminalController()
for i in range(args.validation_size):
    p = (model.predict(np.expand_dims(X[i], axis=0)))[0][0]
    
    ctr = 0
    for c in range(dimension*dimension):
        I = X[i][ctr]
        sumI[c] += I
        ctr += 1

    sumP += p
    P[i] = p
    if(i % 10 == 0):
        sys.stdout.write('\rRecording prediction for Event %d' %i)
        sys.stdout.flush()
    # sys.stdout.flush()
    # sys.stdout.write(term.BOL + term.CLEAR_EOL)
    # sys.stdout.write('Recording prediction for Event: %d' % i)
print('.')
x_avg = np.divide(sumI, args.validation_size)
p_avg = sumP / args.validation_size

sumDif = np.zeros((dimension*dimension))
sumX = np.zeros((dimension*dimension))
sumP = np.zeros((dimension*dimension))

for i in range(args.validation_size):
    ctr = 0
    for a in range(dimension):
        for b in range(dimension):
            sumDif[ctr] += ((X[i][ctr] - x_avg[ctr]) * (P[i] - p_avg))
            sumX[ctr] += math.pow((X[i][ctr] - x_avg[ctr]),2)
            sumP[ctr] += math.pow((P[i] - p_avg),2)
            ctr+=1
    if(i % 10 == 0):
        sys.stdout.write('\rPreparing Pearson Coeff sums for event %d' %i)
        sys.stdout.flush()
print('.')
ctr = 0
for a in range(dimension):
    for b in range(dimension):
        bot = ((math.sqrt(sumX[ctr])) * (math.sqrt(sumP[ctr])))
        if(bot != 0):
            r = (sumDif[ctr]/bot)
        else:
            r = 1
        histPearson.Fill((-HIST_BOUND_CONE + (a*2*HIST_BOUND_CONE/float(dimension))), (-HIST_BOUND_CONE + (b*2*HIST_BOUND_CONE/float(dimension))), r)
        ctr +=1

canvasPearson = ROOT.TCanvas("canvasPearson", "canvasPearson")
title=args.classes
folder='pearson'
ROOT.gStyle.SetOptStat("")

canvasPearson.cd()
histPearson.Draw("COLZ")
histPearson.SetTitle(title + " NN Pearson Coef")
histPearson.GetXaxis().SetTitle("column")
histPearson.GetYaxis().SetTitle("row")

canvasPearson.SaveAs(folder+ '/' + str(args.validation_size) + '/' +str(args.notes) + title + "_" + str(dimension) + "_NNPearsonCoeff.pdf")
