#!/bin/bash

cd /home/yu.yale.edu/sc2554/JetStuff/JetAnalysis
/usr/bin/python2.7 /home/yu.yale.edu/sc2554/JetStuff/JetAnalysis/LDAJet.py sampleAJetPre.txt sampleBJetPre.txt
echo "AB completed"
/usr/bin/python2.7 /home/yu.yale.edu/sc2554/JetStuff/JetAnalysis/LDAJet.py sampleAJetPre.txt sampleCJetPre.txt
echo "AC completed"
# python LDAJet.py sampleAJetPre.txt sampleDJetPre.txt
# python LDAJet.py sampleBJetPre.txt sampleCJetPre.txt
# python LDAJet.py sampleBJetPre.txt sampleDJetPre.txt
# python LDAJet.py sampleCJetPre.txt sampleDJetPre.txt
# python LDAJet.py sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt
# python LDAJet.py sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt
# python LDAJet.py sampleAJetPre.txt sampleBJetPre.txt sampleDJetPre.txt
# python LDAJet.py sampleAJetPre.txt sampleBJetPre.txt sampleCJetPre.txt sampleDJetPre.txt
