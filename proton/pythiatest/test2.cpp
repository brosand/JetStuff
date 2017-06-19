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

using namespace std;
using namespace Pythia8;

int main(){

cout<< "\n\n\n\n****************Hello World!*****************\n\n\n\n" << endl;

Pythia obj;

	//from leadtree3
	int iEvents, nEvents, iFinalParticles, nFinalParticles;
	cout << "Enter the number of events: ";
        cin >> nEvents;
	double px[nFinalParticles], py[nFinalParticles], pz[nFinalParticles], energy[nFinalParticles];
	int charge[nFinalParticles];

	//create a tree and link it
	TTree tree("tree", "tree with event data and particle data in arrays");
	tree.Branch("iEvents", &iEvents, "iEvents/I");
	tree.Branch("nFinalParticles", &nFinalParticles, "nFinalParticles/I");
	tree.Branch("px", &px, "px[nFinalParticles]/F");
	tree.Branch("py", &py, "py[nFinalParticles]/F");
	tree.Branch("pz", &pz, "pz[nFinalParticles]/F");
	tree.Branch("energy", &energy, "energy[nFinalParticles]/F");
	tree.Branch("charge", &charge, "charge[nFinalParticles]/I");

//tell it what is particle 1 and 2, using the PDG code
obj.readString("Beams:idA = 2212");
obj.readString("Beams:idB = 2212");

//tell it energy
obj.readString("Beams:eCM = 2760");

//tell it the frame type
obj.readString("Beams:frameType = 1");

//
obj.readString("SoftQCD:all = on");
obj.init();

//set up my chart
cout << "event\tParticleNo.\tp_x\tp_y\tp_z\tenergy\tcharge\n";

//how many events do you want? Somehow need this to see events

for (iEvents = 0; iEvents < nEvents; ++iEvents){
//do I need this loop layer for the tree?
	nFinalParticles = 0; //reset this for each event
	iFinalParticles = 0;
	obj.next(); //first time called it prints out event list, but later times it is called it does not
	cout << iEvents <<endl;
	obj.event.list();
	cout << "-------" << endl;

	for (int i = 0; i < obj.event.size(); ++i){ 

		if (obj.event[i].isFinal()){

			iFinalParticles++;
			
		//if its final, add event to tree

			px[iFinalParticles] = obj.event[i].px();
			py[iFinalParticles] = obj.event[i].py();
			pz[iFinalParticles] = obj.event[i].pz();
			energy[iFinalParticles] = obj.event[i].e();
			charge[iFinalParticles] = obj.event[i].charge();

			//keep a running total of number of final particles

							
			
			cout << iEvents << "\t" << i << "\t" << obj.event[i].px() << "\t" << obj.event[i].py() << "\t" << obj.event[i].pz() << "\t" << obj.event[i].e() << "\t" << obj.event[i].charge()<< endl;

		}

		nFinalParticles = iFinalParticles;
	}

	tree.Fill();
}
tree.Print();
//write the tree to a file
TFile f("ppfile.root", "recreate");
tree.Write();
//f.ls();
f.Close();

return 0;
		
}
