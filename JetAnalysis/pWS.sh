#!/bin/sh
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/B21.txt --architecture=waNNModels/ABmodel.json --weights=waNNModels/ABweights.h5 --validation_size=2000 --classes=AB --range=0

python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/C21.txt --architecture=waNNModels/ACmodel.json --weights=waNNModels/ACweights.h5 --validation_size=2000 --classes=AC --range=0
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/D21.txt --architecture=waNNModels/ADmodel.json --weights=waNNModels/ADweights.h5 --validation_size=2000 --classes=AD --range=0

python wPixelWeight.py --data=r1.0/B21.txt --data1=r1.0/C21.txt --architecture=waNNModels/BCmodel.json --weights=waNNModels/BCweights.h5 --validation_size=2000 --classes=BC --range=0
python wPixelWeight.py --data=r1.0/B21.txt --data1=r1.0/D21.txt --architecture=waNNModels/BDmodel.json --weights=waNNModels/BDweights.h5 --validation_size=2000 --classes=BD --range=0

python wPixelWeight.py --data=r1.0/C21.txt --data1=r1.0/D21.txt --architecture=waNNModels/CDmodel.json --weights=waNNModels/CDweights.h5 --validation_size=2000 --classes=CD --range=0python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/B21.txt --architecture=waNNModels/ABmodel.json --weights=waNNModels/ABweights.h5 --validation_size=2000 --classes=AB --range=1
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/C21.txt --architecture=waNNModels/ACmodel.json --weights=waNNModels/ACweights.h5 --validation_size=2000 --classes=AC --range=1
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/D21.txt --architecture=waNNModels/ADmodel.json --weights=waNNModels/ADweights.h5 --validation_size=2000 --classes=AD --range=1
python wPixelWeight.py --data=r1.0/B21.txt --data1=r1.0/C21.txt --architecture=waNNModels/BCmodel.json --weights=waNNModels/BCweights.h5 --validation_size=2000 --classes=BC --range=1
python wPixelWeight.py --data=r1.0/B21.txt --data1=r1.0/D21.txt --architecture=waNNModels/BDmodel.json --weights=waNNModels/BDweights.h5 --validation_size=2000 --classes=BD --range=1
python wPixelWeight.py --data=r1.0/C21.txt --data1=r1.0/D21.txt --architecture=waNNModels/CDmodel.json --weights=waNNModels/CDweights.h5 --validation_size=2000 --classes=CD --range=1
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/B21.txt --architecture=waNNModels/ABmodel.json --weights=waNNModels/ABweights.h5 --validation_size=2000 --classes=AB --range=3
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/C21.txt --architecture=waNNModels/ACmodel.json --weights=waNNModels/ACweights.h5 --validation_size=2000 --classes=AC --range=3
python wPixelWeight.py --data=r1.0/A21.txt --data1=r1.0/D21.txt --architecture=waNNModels/ADmodel.json --weights=waNNModels/ADweights.h5 --validation_size=2000 --classes=AD --range=3
python wPixelWeight.py --data=r1.0/B21.txt --data1=r1.0/C21.txt --architecture=waNNModels/BCmodel.json --weights=waNNModels/BCweights.h5 --validation_size=2000 --classes=BC --range=3
python wPixelWeight.py --data=r1.0/B21.txt --data1=r1.0/D21.txt --architecture=waNNModels/BDmodel.json --weights=waNNModels/BDweights.h5 --validation_size=2000 --classes=BD --range=3
python wPixelWeight.py --data=r1.0/C21.txt --data1=r1.0/D21.txt --architecture=waNNModels/CDmodel.json --weights=waNNModels/CDweights.h5 --validation_size=2000 --classes=CD --range=3
