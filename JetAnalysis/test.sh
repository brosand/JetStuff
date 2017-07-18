
#!/bin/sh

echo "hello world"

# python NNJet.py 2 aJetPre.txt bJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
# echo "DNN ab done"
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

python CNNJet.py 2 aJetPre.txt bJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "CNN ab done"
python CNNJet.py 2 aJetPre.txt cJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "CNN ac done"
python CNNJet.py 2 aJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "CNN ad done"
python CNNJet.py 2 bJetPre.txt cJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "CNN bc done"
python CNNJet.py 2 bJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "CNN bd done"
python CNNJet.py 2 cJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 2 nNodes 100
echo "CNN cd done"
