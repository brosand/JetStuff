#!/bin/bash

python pre.py sampleA.root r1.0/sampleAJet.root collisionType=A dimension=50 folder=r1.0
echo "A preprocessing completed."
python pre.py sampleB.root r1.0/sampleBJet.root collisionType=B dimension=50 folder=r1.0
echo "B preprocessing completed."
python pre.py sampleC.root r1.0/sampleCJet.root collisionType=C dimension=50 folder=r1.0
echo "C preprocessing completed."
python pre.py sampleD.root r1.0/sampleDJet.root collisionType=D dimension=50 folder=r1.0
echo "D preprocessing completed."
python pre.py pp.root r1.0/ppJet.root collisionType=pp dimension=50 folder=r1.0
echo "pp preprocessing completed."
#python pre.py w.root r1.0/wJet.root collisionType=w dimension=5 folder=r1.0
#echo "w preprocessing completed."
#python pre.py lead.root r1.0/lead.root collisionType=lead dimension=5 folder=r1.0
#echo "leadfake preprocessing completed."
