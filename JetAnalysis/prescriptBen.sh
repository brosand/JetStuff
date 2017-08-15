#!/bin/bash

python prept.py --data=sampleA.root --jets=r1.0/sampleAJet.root --type=A --dim=11 --folder=r1.0
echo "A preprocessing completed."
python prept.py --data=sampleB.root --jets=r1.0/sampleBJet.root --type=B --dim=11 --folder=r1.0
echo "B preprocessing completed."
python prept.py --data=sampleC.root --jets=r1.0/sampleCJet.root --type=C --dim=11 --folder=r1.0
echo "C preprocessing completed."
python prept.py --data=sampleD.root --jets=r1.0/sampleDJet.root --type=D --dim=11 --folder=r1.0
echo "D preprocessing completed."
python prept.py --data=pp.root --jets=r1.0/ppJet.root --type=pp --dim=11 --folder=r1.0
echo "pp preprocessing completed."
python prept.py --data=w.root --jets=r1.0/wJet.root --type=w --dim=11 --folder=r1.0
#echo "w preprocessing completed."
python prept.py --data=lead.root --jets=r1.0/leadJet.root --type=lead --dim=11 --folder=r1.0
#echo "leadfake preprocessing completed."

