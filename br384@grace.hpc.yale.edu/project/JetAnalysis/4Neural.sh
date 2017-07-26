python NNJet.py 4 aJetPre.txt bJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5 inputDim 5 numClasses 4 nNodes 100 verbose 1
#!/bin/sh

python CNNJet.py 4 aJetPre.txt bJetPre.txt cJetPre.txt dJetPre.txt nEpochs 5 verbose 1
python NNJet.py 4 sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5 inputDim 10 numClasses 4 nNodes 100 verbose 1
python CNNJet.py 4 sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt nEpochs 5 verbose 1
