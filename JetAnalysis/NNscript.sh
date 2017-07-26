
#!/bin/sh

# python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
# echo "DNN ab done"
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN ac done"
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN ac done"
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN ad done"
python NNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN bc done"
python NNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN bd done"
python NNJet.py r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN cd done"

python CNNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt nEpochs 5
echo "CNN ab done"
python CNNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5
echo "CNN ac done"
python CNNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5
echo "CNN ad done"
python CNNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5
echo "CNN bc done"
python CNNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5
echo "CNN bd done"
python CNNJet.py r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5
echo "CNN cd done"



python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN abcd done"
python CNNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5
echo "CNN abcd done"

python NNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN bcd done"
python CNNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5
echo "CNN bcd done"

python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN acd done"
python CNNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5
echo "CNN acd done"

python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN abd done"
python CNNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5
echo "CNN abd done"

python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN abc done"
python CNNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5
echo "CNN abc done"




#10x10

python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN ac done"
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN ac done"
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN ad done"
python NNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN bc done"
python NNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN bd done"
python NNJet.py r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN cd done"

python CNNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt nEpochs 5
echo "CNN ab done"
python CNNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5
echo "CNN ac done"
python CNNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5
echo "CNN ad done"
python CNNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5
echo "CNN bc done"
python CNNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5
echo "CNN bd done"
python CNNJet.py r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5
echo "CNN cd done"



python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN abcd done"
python CNNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5
echo "CNN abcd done"

python NNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN bcd done"
python CNNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5
echo "CNN bcd done"

python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN acd done"
python CNNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5
echo "CNN acd done"

python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN abd done"
python CNNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5
echo "CNN abd done"

python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
echo "DNN abc done"
python CNNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5
echo "CNN abc done"






# python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt nEpochs 5 nNodes 100 nLayers 3
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleAJetPre20.txt r1.0/sampleBJetPre20.txt r1.0/sampleCJetPre20.txt r1.0/sampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1
python NNJet.py r1.0/sampleSampleAJetPre20.txt r1.0/sampleSampleBJetPre20.txt r1.0/sampleSampleCJetPre20.txt r1.0/sampleSampleDJetPre20.txt nEpochs 5 nNodes 100 nLayers 1