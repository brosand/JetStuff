from __future__ import print_function
import PIL
import numpy as np
import pandas
import math
import argparse
import json
import ROOT

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
parser.add_argument('--data', default='r1.0/sampleAJetPre21_pt.txt', help="dataset to be tested on")
parser.add_argument('--data1', default='r1.0/sampleBJetPre21_pt.txt', help="second dataset to be tested on")
parser.add_argument('--weights', default='weights.h5' , help="weights of model")
parser.add_argument('--architecture', default='model.json' , help="architecture of model")
parser.add_argument('--validation_size', default=1000, help="number of jets", type=int)
parser.add_argument('--classes', default='', help="classes of data")
parser.add_argument('--notes', default='', help="notes")
parser.add_argument('--draw', default=0, type=int, help="0: draw coeffs, 1: draw probability, 2: draw both")
parser.add_argument('--range', default=1, type=int, help="range of output histogram (0-->automatic)")

args = parser.parse_args()

if (args.classes==''):
    args.classes=raw_input('Enter classes: ')

dataset1 = pandas.read_csv(args.data ,sep=" ",header=None)
array1 = dataset.values
dimension = (array[0, 1])

dataset2 = pandas.read_csv(args.data1 ,sep=" ",header=None)
array2 = dataset1.values

histPaerson = ROOT.TH2F("histPearson", "Pearson Coefficient Histogram", dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE, dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE)

X1 = array1[: , 2:(dimension*dimension) + 2]  
X2 = array2[: , 2:(dimension*dimension) + 2]  

X1 = X1[:args.validation_size]
X2 = X2[:args.validation_size]
P = np.zeros((validation_size,NUM_CLASSES))


json_file = open(args.architecture, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(args.weights)
print('Number of test cases, dimensioN: ' + str(X.shape))

sumP1 = 0
sumP2 = 0
sumI1 = 0
sumI2 = 0

sumI1 = np.zeros((dimension))
sumI2 = np.zeros((dimension))


for i in range(validation_size):
    p1 = (model.predict(np.expand_dims(X1[i], axis=0)))[0][0]
    p2 = (model.predict(np.expand_dims(X2[i], axis=0)))[0][1]
    
    ctr = 0
    for c in range(dimension*dimension):
        i1 = X1[i][ctr]
        i2 = X2[i][ctr]
        sumI1[c] += i1
        sumI2[c] += i2
        ctr += 1

    sumP1 += p1
    sumP2 += p2
    P[i,0] = p1
    P[i,1] = p2

x1_avg = np.divide(sumI1, validation_size)
y1_avg = sumP1 / validation_size

x2_avg = np.divide(sumI2, validation_size)
y2_avg = sumP2 / validation_size

# r1 = np.zeros((dimension*dimension))
# r2 = np.zeros((dimension*dimension))
sumDif1 = np.zeros((dimension*dimension))
sumX1 = np.zeros((dimension*dimension))
sumY1 = np.zeros((dimension*dimension))

sumDif2 = np.zeros((dimension*dimension))
sumX2 = np.zeros((dimension*dimension))
sumY2 = np.zeros((dimension*dimension))

for i in range(validation_size):
    ctr = 0
    for a in range(dimension):
        for b in range(dimension):
            sumDif1 += ((X[ctr] - x1_avg) * (P[ctr][0] - y1_avg))
            sumDif2 += ((X1[ctr] - x2_avg) * (P[ctr][1] - y2_avg))
            sumX1 += math.pow((X1[ctr] - x1_avg),2)
            sumX2 += math.pow((X2[ctr] - x2_avg),2)
            sumY1 += math.pow((P[ctr][0] - Y1_avg),2)
            sumY2 += math.pow((P[ctr][1] - Y2_avg),2)

for a in range(dimension):
    for b in range(dimension):
        bot = ((math.sqrt(sumX1)) * (math.sqrt(sumY1)))
        r1 = (sumDif1/bot)
        histPearson.Fill((-HIST_BOUND_CONE + (a*2*HIST_BOUND_CONE/float(dimension))), (-HIST_BOUND_CONE + (b*2*HIST_BOUND_CONE/float(dimension))), bot)

canvasPearson = ROOT.TCanvas("canvasPearson", "canvasPearson")

title=args.classes
folder='pearson'
logbase=10
ROOT.gStyle.SetOptStat("")

canvasPearson.cd()
histPearson.Draw("COLZ")
histPearson.SetTitle(title + " NN Coef")
histPearson.GetXaxis().SetTitle("column")
histPearson.GetYaxis().SetTitle("row")

canvasPearson.SaveAs(folder+str(args.validation_size) + '/' +str(args.notes) + title + "_" + str(dimension) + "_NNPearsonCoeff.pdf")