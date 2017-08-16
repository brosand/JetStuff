#include "/home/yu.yale.edu/br384/fastjet-3.2.2/include/fastjet/ClusterSequence.hh"
#include "/home/yu.yale.edu/br384/fastjet-3.2.2/include/fastjet/PseudoJet.hh"
#include <iostream>
#include <stdlib.h>

#include <TF1.h>
#include "TTree.h"
#include "TFile.h"
#include "TTreeReader.h"
#include <TTreeReaderArray.h>


using namespace fastjet;
using namespace std;

int main (){
	
	

	int nEvents = 0;
  //create a reader to interpret the TTree
	TFile *f = TFile::Open("ppfile.root");	
	
	if (f == 0) {
		cout << "Error. Could not open file." << endl;
		return 1;
	}

	TTreeReader myReader("tree" ,f);
	TTreeReaderArray<double> myPx(myReader, "px");
	TTreeReaderArray<double> myPy(myReader, "py");
	TTreeReaderArray<double> myPz(myReader, "pz");
	TTreeReaderArray<double> myEnergy(myReader, "energy");
	TTreeReaderValue<int> myEvents(myReader, "iEvents");
	TTreeReaderValue<int> myNFinalParticles(myReader, "nFinalParticles");

  //Pseudojet vector
  //vector of pseudoJets
	// vector<vector<PseudoJet>> particlesVector;
  //loop through the particles and turn them into pseudojets
	while(myReader.Next()) {
//Note For Understanding: myReader.Next() --> iterates through the first level of the reader, or the only level for the value reader, the array reader needs to levels (understanding as of 6/20/17)

		vector<PseudoJet> particles;			
		for (int i = 0; i < *myNFinalParticles; i++)
		{

			particles.push_back(PseudoJet(myPx[i], myPy[i], myPz[i], myEnergy[i]));
		}

 
  // choose a jet definition
		double R = 0.6;

		JetDefinition jet_def(antikt_algorithm, R);
  // run the clustering, extract the jets
		ClusterSequence cs(particles, jet_def);
		vector<PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());
  // print out some infos
		cout << "Clustering with " << jet_def.description() << endl;
  // print the jets
		cout << "Event #" << nEvents << endl;
		cout <<   "        pt y phi" << endl;
		for (unsigned i = 0; i < jets.size(); i++) {
			cout << "jet " << i << ": "<< jets[i].pt() << " " 
			<< jets[i].rap() << " " << jets[i].phi() << endl;
			vector<PseudoJet> constituents = jets[i].constituents();
			for (unsigned j = 0; j < constituents.size(); j++) {
				cout << "    constituent " << j << "'s pt: " << constituents[j].pt()      << endl;
			}
		}
		
		nEvents++;
		// particlesVector.push_back(particles);
	} 
	// return 1;
}

	//resolution/code radius --.6
