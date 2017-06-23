#include "/home/yu.yale.edu/br384/fastjet-3.2.2/include/fastjet/ClusterSequenceArea.hh"
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
	TTreeReaderArray<double> numParticles(myReader, "nFinalParticles")
	TTreeReaderValue<int> myEvents(myReader, "iEvents");
	TTreeReaderValue<int> myNFinalParticles(myReader, "nFinalParticles");

	vector<int> pt, y, phi, area;
	//y is rapidity

	int	eventN, nJets;


    //create output TTree
    TTree tree("tree", "ttree with jet data");
    tree.Branch("eventN", &eventN, "eventN/I");
    tree.Branch("nJets", &nJets, "nJets/I");
    tree.Branch("pt", &pt);
    tree.Branch("y", &y);
    tree.Branch("phi", &phi);
    tree.Branch("area", &area);
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
		AreaDefinition area_def(voronoi_area);

  // run the clustering, extract the jets
		ClusterSequenceArea cs(particles, jet_def, area_def);
		vector<PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());
  //add the jet data to the final TTree

		for (unsigned i = 0; i < jets.size(); i++) {
			pt.push_back(jets[i].pt());
			y.push_back(jets[i].phi());
			phi.push_back(jets[i].rap());
			area.push_back(jets[i].area());

			// cout << "jet " << i << ": "<< jets[i].pt() << " " 
			// << jets[i].rap() << " " << jets[i].phi() << endl;
			// vector<PseudoJet> constituents = jets[i].constituents();
			// for (unsigned j = 0; j < constituents.size(); j++) {
			// 	cout << "    constituent " << j << ""s pt: " << constituents[j].pt()      << endl;
			}
		}
		
		// particlesVector.push_back(particles);
	} 

	// return 1;


	//resolution/code radius --.6

