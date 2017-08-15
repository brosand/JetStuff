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
# from keras.model import predict
parser = argparse.ArgumentParser()
parser.add_argument('--data', default='r1.0/sampleAJetPre21_pt.txt', help="dataset to be tested on")
parser.add_argument('--data1', default='r1.0/sampleBJetPre21_pt.txt', help="second dataset to be tested on")
parser.add_argument('--model', default='NNModels/NNModel17:21:46' , help="model to analyze")
parser.add_argument('--validation_size', default=1000, help="number of jets", type=int)
parser.add_argument('--classes', default='', help="classes of data")

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
model = load_model(args.model)
# print(outArray)
print(X.shape)
tot=0
tot1=0
for i in range(len(X)):
    # print((np.expand_dims(X[i], axis=0)).shape) 
    # print((model.predict(np.expand_dims(X[i], axis=0)))[0][0])
    if (((model.predict(np.expand_dims(X[i], axis=0)))[0][0]) < .5):
         aguess -=  1

    ctr = 0
    p = (model.predict(np.expand_dims(X[i], axis=0)))[0][0]
    p1 = (model.predict(np.expand_dims(X1[i], axis=0)))[0][1]

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
            outArray[b,a] += (c)
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
    if(i % 100 == 0):
        print('Event: %d' % i)
        print(outArray[10][10])
        # print((X[i][0])*(p))
# print('break')
# print(normalize(outArray))
for a, i in enumerate(outArray):
     for b, c in enumerate(i):
        if (c[0] < 0):
            outArray[a,b,1] = np.log(abs(c[0]) + 1)
            outArray[a,b,0] = 0
            tot +=outArray[a,b,1]
        else:
            outArray[a,b,0] = np.log(c[0] + 1)
            tot +=outArray[a,b,0]

print(outArray)
imsave(('test.jpg'), (outArray))
MULTIPLIER = 40
img = Image.open('test.jpg')
# img=img.rotate(90)
imgOut = Image.new(mode='RGB',size=(MULTIPLIER*dimension,MULTIPLIER*dimension))


# print(img.size[0])
# print(img.size[1])
# tmpArray = []
# for a in range(dimension):
#     if (a % 10 == 0):
#         print(a)
#     for b in range(img.size[1]):
#         for c in range((a*MULTIPLIER),((a+1)*MULTIPLIER)):
#             for d in range((b*MULTIPLIER),((b+1)*MULTIPLIER)):
#                 tmpR=int((255*outArray[a,b,0]/tot))
#                 tmpG=int((255*outArray[a,b,1]/tot))
#                 tmpB=int((255*outArray[a,b,2]/tot))
#                 imgOut.putpixel((c,d), (tmpR,tmpG,tmpB))



# w,h = len(data[0],data[1])
# a = np.zeros((h,w,3),dtype=np.uint8)
# for a in range(w):
#     for b in range(h):
#         a[a][b]=data[a][b]
# imgOut =Image.fromarray(a,'RGB')
imgOut.save('coeff%s.jpg' % args.classes)
print(aguess)
print(args.validation_size)
print(aguess/args.validation_size)


canvasCoef = ROOT.TCanvas("canvasCoef", "canvasCoef")
canvasCoefLog = ROOT.TCanvas("canvasCoefLog", "canvasCoefLog")
title=args.classes
folder='coeffs'
logbase=10
ROOT.gStyle.SetOptStat("")

ZRANGE=.25
canvasCoef.cd()
histogramCOEF.Draw("COLZ")
histogramCOEF.SetTitle(title + " NN Coef")
histogramCOEF.GetXaxis().SetTitle("column")
histogramCOEF.GetYaxis().SetTitle("row")
histogramCOEF.GetZaxis().SetTitle("NN Coef of that pixel")
histogramCOEF.SetMaximum(ZRANGE)
histogramCOEF.SetMinimum(-1*ZRANGE)


# histogramCOEF.GetZaxis().SetLimits(-2,2)
canvasCoef.SaveAs(folder+str(args.validation_size) + "/" + title + "_" + str(dimension) +'r'+ str(ZRANGE) + "_NNCoef.pdf")

canvasCoefLog.cd()
histogramCOEFLog.Draw("COLZ")
histogramCOEFLog.SetTitle(title + " NN Coef Log")
histogramCOEFLog.GetXaxis().SetTitle("column")
histogramCOEFLog.GetYaxis().SetTitle("row")
histogramCOEFLog.GetZaxis().SetTitle("log(NN Coef of that pixel)")
histogramCOEFLog.SetMaximum(ZRANGE)
histogramCOEFLog.SetMinimum(-1*ZRANGE)

canvasCoefLog.SaveAs(folder+str(args.validation_size) + "/" + title + "_" + str(dimension) +'r'+ str(ZRANGE) +'b'+str(logbase)+ "_NNCoef.pdf")


