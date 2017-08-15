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

#f args.model:
#    modelfile = args.model
#else:
#    modelfile = 'NNModels/NNModel14:18:47.h5'
#if args.validation_size:
#    validation_size = args.validation_size
#else:
#    validation_size = 50
# validation_size=50
#with open('model.json') as f:
#  modeljson = json.load(f)
#model=model_from_json(modeljson)
# weights = open('weights.h5', 'r')
#model.load_weights('weights.h5')
# canvasCoef = ROOT.TCanvas("canvasCoef", "canvasCoef")
# canvasCoefLog = ROOT.TCanvas("canvasCoefLog", "canvasCoefLog")

dataset = pandas.read_csv(args.data ,sep=" ",header=None)
array = dataset.values
dimension = (array[0, 1])
dataset1 = pandas.read_csv(args.data1 ,sep=" ",header=None)
array1 = dataset1.values

histogramCOEF = ROOT.TH2F("histogramCOEF", "histogramCOEF", dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE, dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE)
histogramCOEFLog = ROOT.TH2F("histogramCOEFLog", "histogramCOEFLog", dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE, dimension, -HIST_BOUND_CONE, HIST_BOUND_CONE)
histProb1=ROOT.TH1F('histProb1', 'Probability Distribution of Guess ' +str(args.classes[:1] + ' for true sample in ' +str(args.classes) ), 20, 0, 1)
histProb2=ROOT.TH1F('histProb2', 'Probability Distribution of Guess ' +str(args.classes[1:2] + ' for true sample in ' +str(args.classes) ), 20, 0, 1)

seed = 7
np.random.seed(seed)

# print("Dimension: %d" % dimension) 
# dimension=21

X = array[: , 2:(dimension*dimension) + 2]  
X1 = array1[: , 2:(dimension*dimension) + 2]  


# Y = array[: , 0]
# Z = array[: , dimension + 2:dimension + 4]

# encoder = LabelEncoder()
# encoder.fit(Y)
# encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
# dummy_y = np_utils.to_categorical(encoded_Y)


X = X[:args.validation_size]
X1 = X1[:args.validation_size]

aguess = args.validation_size

outArray = np.zeros((dimension,dimension,3))

json_file = open(args.architecture, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# weights = open('weights.h5', 'r')
model.load_weights(args.weights)
# print(outArray)
print(X.shape)
for i in range(len(X)):
    
    # print((np.expand_dims(X[i], axis=0)).shape) 
    # print((model.predict(np.expand_dims(X[i], axis=0)))[0][0])
    if (((model.predict(np.expand_dims(X[i], axis=0)))[0][0]) < .5):
         aguess -=  1

    ctr = 0
    # p = (model.predict(np.expand_dims(X[i], axis=0)))[0][0]
    # p1 = (model.predict(np.expand_dims(X1[i], axis=0)))[0][1]
    # print('probs')
    p = 1
    p1 = 0
    # print(p)
    # print(p1)
    histProb1.Fill(p)
    histProb2.Fill(p1)

    # p=1
    for a in range(dimension):
        # print(a)
        for b in range(dimension):
                # print(a)
                # print(b)
            # print(model.predict(np))
            # X = np.expand_dims(X[i], axis=0)
            # print(b)
            # print(a*dimension+b)
#DOUBLE CHECK WHICH IS A AND WHICH IS B
            # c = ((X[i][((b * dimension) + a - 1)])*(p))
            c = ((((X[i][ctr])*(p))) - (X1[i][ctr])*(p1))   
            # c=X[i][ctr]       
             # outArray[b,a] += (c)
            # if(a==b==10 ):
            #     c=0
            # if(a==9 and b==10 ):
            #     c=0
            # histogramCOEF.Fill(a,b, c)
            histogramCOEF.Fill((-HIST_BOUND_CONE + (a*2*HIST_BOUND_CONE/float(dimension))), (-HIST_BOUND_CONE + (b*2*HIST_BOUND_CONE/float(dimension))), c)
#add one inside of log to avoid small numbers outweighing large ones
            if (c < 0):
               d = (-1 * (np.log10((abs(c) + 1))))
            else:
                d=np.log10(c+1)     
            # histogramCOEFLog.Fill(a,b, d)
            histogramCOEFLog.Fill((-HIST_BOUND_CONE + (a*2*HIST_BOUND_CONE/float(dimension))), (-HIST_BOUND_CONE + (b*2*HIST_BOUND_CONE/float(dimension))), d)

            ctr += 1
            # print(ctr)
            # d = outArray[a][b]
            # print(c)
            # print(outArray[a,b])
            sys.stdout.write('\rEvent: %d' % i)
            sys.stdout.flush()
        # print(outArray[10][10])
        # print((X[i][0])*(p))
# print('break')
# print(normalize(outArray))
# for a, i in enumerate(outArray):
#      for b, c in enumerate(i):
#         if (c[0] < 0):
#             outArray[a,b,1] = np.log(abs(c[0]) + 1)
#             outArray[a,b,0] = 0
#             tot +=outArray[a,b,1]
#         else:
#             outArray[a,b,0] = np.log(c[0] + 1)
#             tot +=outArray[a,b,0]

# print(outArray)
# imsave(('test.jpg'), (outArray))
# MULTIPLIER = 40
# img = Image.open('test.jpg')
# # img=img.rotate(90)
# imgOut = Image.new(mode='RGB',size=(MULTIPLIER*dimension,MULTIPLIER*dimension))


# # print(img.size[0])
# # print(img.size[1])
# # tmpArray = []
# # for a in range(dimension):
# #     if (a % 10 == 0):
# #         print(a)
# #     for b in range(img.size[1]):
# #         for c in range((a*MULTIPLIER),((a+1)*MULTIPLIER)):
# #             for d in range((b*MULTIPLIER),((b+1)*MULTIPLIER)):
# #                 tmpR=int((255*outArray[a,b,0]/tot))
# #                 tmpG=int((255*outArray[a,b,1]/tot))
# #                 tmpB=int((255*outArray[a,b,2]/tot))
# #                 imgOut.putpixel((c,d), (tmpR,tmpG,tmpB))



# # w,h = len(data[0],data[1])
# # a = np.zeros((h,w,3),dtype=np.uint8)
# # for a in range(w):
# #     for b in range(h):
# #         a[a][b]=data[a][b]
# # imgOut =Image.fromarray(a,'RGB')
# imgOut.save('coeff%s.jpg' % args.classes)
# print(aguess)
# print(args.validation_size)
# print(aguess/args.validation_size)
print('')
canvasProb1 = ROOT.TCanvas('histProb1', 'histProbT')
canvasProb2 = ROOT.TCanvas('histProb2', 'histProbT2')

canvasCoef = ROOT.TCanvas("canvasCoef", "canvasCoef")
canvasCoefLog = ROOT.TCanvas("canvasCoefLog", "canvasCoefLog")
title=args.classes
folder='coeffs'
logbase=10
ROOT.gStyle.SetOptStat("")
for row in range(dimension):
    for col in range(dimension):
            # print(histogramCOEFLog.GetBinContent(row,col)) 
            if ((-1 * histogramCOEFLog.GetBinContent(row,col)) > args.range):
                histogramCOEFLog.SetBinContent(row,col, -1 * args.range)
if (args.draw==1 or args.draw==2):
    canvasProb1.cd()
    histProb1.Draw()
    canvasProb1.SaveAs('probDist/'+str(args.notes) + title + "_" + title[:1] + str(dimension) + "prob.pdf")

    canvasProb2.cd()
    histProb2.Draw()
    canvasProb2.SaveAs('probDist/'+str(args.notes) + title + "_" + title[1:2] + str(dimension) + "prob.pdf")
if (args.draw==0 or args.draw==2):
    canvasCoef.cd()
    histogramCOEF.Draw("COLZ")
    histogramCOEF.SetTitle(title + " NN Coef")
    histogramCOEF.GetXaxis().SetTitle("column")
    histogramCOEF.GetYaxis().SetTitle("row")
    histogramCOEF.GetZaxis().SetTitle("NN Coef of that pixel")
    if(args.range!=0):
        histogramCOEF.SetMaximum(args.range)
        histogramCOEF.SetMinimum(-1*args.range)


    # histogramCOEF.GetZaxis().SetLimits(-2,2)
    canvasCoef.SaveAs(folder+str(args.validation_size) + "/r" +str(args.range)+ '/' +str(args.notes) + title + "_" + str(dimension) + "_NNCoef.pdf")

    canvasCoefLog.cd()
    histogramCOEFLog.Draw("COLZ")
    histogramCOEFLog.SetTitle(title + " NN Coef Log")
    histogramCOEFLog.GetXaxis().SetTitle("column")
    histogramCOEFLog.GetYaxis().SetTitle("row")
    histogramCOEFLog.GetZaxis().SetTitle("log(NN Coef of that pixel)")
    if(args.range!=0):
        histogramCOEFLog.SetMaximum(args.range)
        histogramCOEFLog.SetMinimum(-1*args.range)
    canvasCoefLog.SaveAs(folder+str(args.validation_size) + "/r" +str(args.range)+"/"+str(args.notes) + title + "_" + str(dimension) +'b'+str(logbase)+ "_NNCoefLog.pdf")
#ALL LOG FOR FINAL IS BASE 10
