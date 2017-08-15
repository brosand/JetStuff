
#!/bin/sh



python NNJet.py r1.0/A21.txt r1.0/B21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes AB
python NNJet.py r1.0/A21.txt r1.0/C21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes AC
python NNJet.py r1.0/A21.txt r1.0/D21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes AD
python NNJet.py r1.0/B21.txt r1.0/C21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes BC
python NNJet.py r1.0/B21.txt r1.0/D21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes BD
python NNJet.py r1.0/C21.txt r1.0/D21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes CD
python NNJet.py r1.0/B21.txt r1.0/C21.txt r1.0/D21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes BCD
python NNJet.py r1.0/A21.txt r1.0/C21.txt r1.0/D21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes ACD
python NNJet.py r1.0/A21.txt r1.0/B21.txt r1.0/D21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes ABD
python NNJet.py r1.0/A21.txt r1.0/B21.txt r1.0/C21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes ABC
python NNJet.py r1.0/a21.txt r1.0/b21.txt r1.0/c21.txt r1.0/d21.txt nEpochs 4 nNodes 300 nLayers 3 verbose 1 classes ABCD
