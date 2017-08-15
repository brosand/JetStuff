#!/bin/sh

python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/B21.txt --architecture=waNNModels/ABmodel.json --weights=waNNModels/ABweights.h5 --validation_size=2000 --classes=AB --draw=1
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/C21.txt --architecture=waNNModels/ACmodel.json --weights=waNNModels/ACweights.h5 --validation_size=2000 --classes=AC --draw=1
python pearsonCalc.py --data=r1.0/A21.txt --architecture=waNNModels/ADmodel.json --weights=waNNModels/ADweights.h5 --validation_size=40000 --classes=AD
python pearsonCalc.py --data=r1.0/B21.txt --architecture=waNNModels/BCmodel.json --weights=waNNModels/BCweights.h5 --validation_size=40000 --classes=BC
python pearsonCalc.py --data=r1.0/B21.txt --architecture=waNNModels/BDmodel.json --weights=waNNModels/BDweights.h5 --validation_size=40000 --classes=BD
python pearsonCalc.py --data=r1.0/C21.txt --architecture=waNNModels/CDmodel.json --weights=waNNModels/CDweights.h5 --validation_size=40000 --classes=CD
