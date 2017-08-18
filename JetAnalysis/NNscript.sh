#!/bin/sh
python NNJet.py --data=r0.2/2R21.txt --data=r1.0/A21.txt --epochs=4 --nodes=400 --layers=3 --classes=.2RB
python NNJet.py --data=r0.2/2R21.txt --data=r1.0/B21.txt --epochs=4 --nodes=400 --layers=3 --classes=.2RB
python NNJet.py --data=r0.2/2R21.txt --data=r1.0/C21.txt --epochs=4 --nodes=400 --layers=3 --classes=.2RC
python NNJet.py --data=r0.2/2R21.txt --data=r1.0/D21.txt --epochs=4 --nodes=400 --layers=3 --classes=.2RD
python NNJet.py --data=r0.2/2R21.txt --data=r1.0/pN21.txt --epochs=4 --nodes=400 --layers=3 --classes=.2RpN

python NNJet.py --data=r1.0/R21.txt --data=r1.0/A21.txt --epochs=4 --nodes=400 --layers=3 --classes=RB
python NNJet.py --data=r1.0/R21.txt --data=r1.0/B21.txt --epochs=4 --nodes=400 --layers=3 --classes=RB
python NNJet.py --data=r1.0/R21.txt --data=r1.0/C21.txt --epochs=4 --nodes=400 --layers=3 --classes=RC
python NNJet.py --data=r1.0/R21.txt --data=r1.0/D21.txt --epochs=4 --nodes=400 --layers=3 --classes=RD
python NNJet.py --data=r1.0/R21.txt --data=r1.0/pN21.txt --epochs=4 --nodes=400 --layers=3 --classes=RpN
