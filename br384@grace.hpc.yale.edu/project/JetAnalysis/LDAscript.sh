#!/bin/bash
cd /home/yu.yale.edu/sc2554/JetStuff/JetAnalysis
python LDAJet.py r1.0/sampleAJetPre5.txt r1.0/sampleBJetPre5.txt r1.0
echo "AB completed"
python LDAJet.py r1.0/sampleAJetPre5.txt r1.0/sampleCJetPre5.txt r1.0
echo "AC completed"
python LDAJet.py r1.0/sampleAJetPre5.txt r1.0/sampleDJetPre5.txt r1.0
echo "AD completed"
python LDAJet.py r1.0/sampleBJetPre5.txt r1.0/sampleCJetPre5.txt r1.0
echo "BC completed"
python LDAJet.py r1.0/sampleBJetPre5.txt r1.0/sampleDJetPre5.txt r1.0
echo "BD completed"
python LDAJet.py r1.0/sampleCJetPre5.txt r1.0/sampleDJetPre5.txt r1.0
echo "CD completed"
python LDAJet.py r1.0/sampleAJetPre5.txt r1.0/sampleBJetPre5.txt r1.0/sampleCJetPre5.txt r1.0
echo "ABC completed"
python LDAJet.py r1.0/sampleBJetPre5.txt r1.0/sampleCJetPre5.txt r1.0/sampleDJetPre5.txt r1.0
echo "BCD completed"
python LDAJet.py r1.0/sampleAJetPre5.txt r1.0/sampleBJetPre5.txt r1.0/sampleDJetPre5.txt r1.0
echo "ABD completed"
python LDAJet.py r1.0/sampleAJetPre5.txt r1.0/sampleBJetPre5.txt r1.0/sampleCJetPre5.txt r1.0/sampleDJetPre5.txt r1.0
echo "ABCD completed"
