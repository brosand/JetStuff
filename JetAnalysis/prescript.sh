#!/bin/bash

python pre.py sampleA.root r1.0/sampleAJet.root r1.0/sampleAJetPre.txt collisionType=A dimension=5
python pre.py sampleB.root r1.0/sampleBJet.root r1.0/sampleBJetPre.txt collisionType=B dimension=5
python pre.py sampleC.root r1.0/sampleCJet.root r1.0/sampleCJetPre.txt collisionType=C dimension=5
python pre.py sampleD.root r1.0/sampleDJet.root r1.0/sampleDJetPre.txt collisionType=D dimension=5
