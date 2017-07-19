
#!/bin/sh

# python NNJet.py 2 aJetPre.txt bJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
# echo "DNN ab done"
python NNJet.py 2 aJetPre.txt bJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "DNN ac done"
python NNJet.py 2 aJetPre.txt cJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "DNN ac done"
python NNJet.py 2 aJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "DNN ad done"
python NNJet.py 2 bJetPre.txt cJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "DNN bc done"
python NNJet.py 2 bJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "DNN bd done"
python NNJet.py 2 cJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "DNN cd done"

python CNNJet.py 2 aJetPre.txt bJetPre.txt nEpochs 5
echo "CNN ab done"
python CNNJet.py 2 aJetPre.txt cJetPre.txt nEpochs 5
echo "CNN ac done"
python CNNJet.py 2 aJetPre.txt dJetPre.txt nEpochs 5
echo "CNN ad done"
python CNNJet.py 2 bJetPre.txt cJetPre.txt nEpochs 5
echo "CNN bc done"
python CNNJet.py 2 bJetPre.txt dJetPre.txt nEpochs 5
echo "CNN bd done"
python CNNJet.py 2 cJetPre.txt dJetPre.txt nEpochs 5
echo "CNN cd done"



python NNJet.py 4 aJetPre.txt bJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 4 nNodes 100
echo "DNN abcd done"
python CNNJet.py 4 aJetPre.txt bJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5
echo "CNN abcd done"

python NNJet.py 3 bJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 4 nNodes 100
echo "DNN bcd done"
python CNNJet.py 3 bJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5
echo "CNN bcd done"

python NNJet.py 3 aJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 4 nNodes 100
echo "DNN acd done"
python CNNJet.py 3 aJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5
echo "CNN acd done"

python NNJet.py 3 aJetPre.txt bJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 3 nNodes 100
echo "DNN abd done"
python CNNJet.py 3 aJetPre.txt bJetPre.txt dJetPre.txt nEpochs 5
echo "CNN abd done"

python NNJet.py 3 aJetPre.txt bJetPre.txt cJetPre.txt nEpochs 5 inputDim 5 numClasses 3 nNodes 100
echo "DNN abc done"
python CNNJet.py 3 aJetPre.txt bJetPre.txt cJetPre.txt nEpochs 5
echo "CNN abc done"




#10x10

python NNJet.py 2 sampleAJetPre.txt sampleBJetPre.txt nEpochs 5 inputDim 10 numClasses 2 nNodes 100
echo "DNN ac done"
python NNJet.py 2 sampleAJetPre.txt sampleCJetPre.txt nEpochs 5 inputDim 10 numClasses 2 nNodes 100
echo "DNN ac done"
python NNJet.py 2 sampleAJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 2 nNodes 100
echo "DNN ad done"
python NNJet.py 2 sampleBJetPre.txt sampleCJetPre.txt nEpochs 5 inputDim 10 numClasses 2 nNodes 100
echo "DNN bc done"
python NNJet.py 2 sampleBJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 2 nNodes 100
echo "DNN bd done"
python NNJet.py 2 sampleCJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 2 nNodes 100
echo "DNN cd done"

python CNNJet.py 2 sampleAJetPre.txt sampleBJetPre.txt nEpochs 5
echo "CNN ab done"
python CNNJet.py 2 sampleAJetPre.txt sampleCJetPre.txt nEpochs 5
echo "CNN ac done"
python CNNJet.py 2 sampleAJetPre.txt sampleDJetPre.txt nEpochs 5
echo "CNN ad done"
python CNNJet.py 2 sampleBJetPre.txt sampleCJetPre.txt nEpochs 5
echo "CNN bc done"
python CNNJet.py 2 sampleBJetPre.txt sampleDJetPre.txt nEpochs 5
echo "CNN bd done"
python CNNJet.py 2 sampleCJetPre.txt sampleDJetPre.txt nEpochs 5
echo "CNN cd done"



python NNJet.py 4 sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 4 nNodes 100
echo "DNN abcd done"
python CNNJet.py 4 sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5
echo "CNN abcd done"

python NNJet.py 3 sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 4 nNodes 100
echo "DNN bcd done"
python CNNJet.py 3 sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5
echo "CNN bcd done"

python NNJet.py 3 sampleAJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 4 nNodes 100
echo "DNN acd done"
python CNNJet.py 3 sampleAJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5
echo "CNN acd done"

python NNJet.py 3 sampleAJetPre.txt sampleBJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 3 nNodes 100
echo "DNN abd done"
python CNNJet.py 3 sampleAJetPre.txt sampleBJetPre.txt sampleDJetPre.txt nEpochs 5
echo "CNN abd done"

python NNJet.py 3 sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt nEpochs 5 inputDim 10 numClasses 3 nNodes 100
echo "DNN abc done"
python CNNJet.py 3 sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt nEpochs 5
echo "CNN abc done"
