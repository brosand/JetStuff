#!/bin/bash

cd /home/yu.yale.edu/sc2554/JetStuff/JetAnalysis
python LDAJet.py sampleAJetPre.txt sampleBJetPre.txt
echo "AB completed"
python LDAJet.py sampleAJetPre.txt sampleCJetPre.txt
echo "AC completed"
python LDAJet.py sampleAJetPre.txt sampleDJetPre.txt
echo "AD completed"
python LDAJet.py sampleBJetPre.txt sampleCJetPre.txt
echo "BC completed"
python LDAJet.py sampleBJetPre.txt sampleDJetPre.txt
echo "BD completed"
python LDAJet.py sampleCJetPre.txt sampleDJetPre.txt
echo "CD completed"
python LDAJet.py sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt
echo "ABC completed"
python LDAJet.py sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt
echo "BCD completed"
python LDAJet.py sampleAJetPre.txt sampleBJetPre.txt sampleDJetPre.txt
echo "ABD completed"
python LDAJet.py sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt
echo "ABCD completed"
