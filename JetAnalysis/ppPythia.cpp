//this is test2
//now make it into trees, so that I can then do histograms

#include "Pythia8/Pythia.h"
#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <TF1.h>
#include "TTree.h"
#include "TH1.h"
#include "TFile.h"
#include "TMath.h"
#include <vector>

using namespace std;
using namespace Pythia8;

int main(){

cout<< "\n\n\n\n****************Hello World!*****************\n\n\n\n" << endl;

Pythia obj;

//from leadtree3
int x = 1, iEvents = 0, nEvents, nFinalParticles;
cout << "Enter the number of events: ";
cin >> nEvents;


vector <double> px;
vector <double> py;
vector <double> pz;
vector <double> energy;
vector <int> charge;
vector <double> mass;

//create a tree and link it
TTree tree("tree", "tree with event data and particle data in arrays");
tree.Branch("iEvents", &iEvents, "iEvents/I");
tree.Branch("nFinalParticles", &nFinalParticles, "nFinalParticles/I");

tree.Branch("px", &px);
tree.Branch("py", &py);
tree.Branch("pz", &pz);
tree.Branch("energy", &energy);
tree.Branch("charge", &charge);
tree.Branch("mass", &mass);

//tell it what is particle 1 and 2, using the PDG code
obj.readString("Beams:idA = 2212");
obj.readString("Beams:idB = 2212");

//tell it energy
obj.readString("Beams:eCM = 2760");

//tell it the frame type
obj.readString("Beams:frameType = 1");

//
obj.readString("HardQCD:all = on");
obj.readString("PhaseSpace:pTHatMin = 20.");

obj.init();

//set up my chart
cout << "event\tParticleNo.\tp_x\tp_y\tp_z\tenergy\tcharge\tmass\n";

for (int iEvents = 0; iEvents < nEvents; iEvents++){
	nFinalParticles = 0; //reset this for each event
	obj.next(); //first time called it prints out event list, but later times it is called it does not
	cout << iEvents << endl;
	//obj.event.list();
	cout << "-------" << endl;
	cout << "event size: " << obj.event.size() << endl;
	for (int i = 0; i < obj.event.size(); i++){ 

		if (obj.event[i].isFinal()){

		//if its final, add event to tree

			//do it with vectors
			px.push_back(obj.event[i].px());
			py.push_back(obj.event[i].py());
			pz.push_back(obj.event[i].pz());
			energy.push_back(obj.event[i].e());
			charge.push_back(obj.event[i].charge());
			mass.push_back(obj.event[i].m());
			
			cout << iEvents << "\t" << i << "\t" << px.at(nFinalParticles) << "\t" << py.at(nFinalParticles) << "\t" << pz.at(nFinalParticles) << "\t" << energy.at(nFinalParticles) << "\t" << charge.at(nFinalParticles) << "\t" << mass.at(nFinalParticles) << endl;
			
			nFinalParticles++;
		}
		
	}
	cout << "Number of Final Particles: " << nFinalParticles << endl;

	tree.Fill();
	px.clear();
	py.clear();
	pz.clear();
	energy.clear();
	charge.clear();
	mass.clear();

	
}
tree.Print();
//write the tree to a file
TFile f("pp.root", "recreate");
tree.Write();
//f.ls();
f.Close();

return 0;
		
}
