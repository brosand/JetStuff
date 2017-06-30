#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/PseudoJet.hh"
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
	TFile a("jetFile.root", "recreate");
	
	if (f == 0) {
		cout << "Error. Could not open file." << endl;
		return 1;
	}

	TTreeReader myReader("tree" ,f);
	TTreeReaderArray<double> myPx(myReader, "px");
	TTreeReaderArray<double> myPy(myReader, "py");
	TTreeReaderArray<double> myPz(myReader, "pz");
	TTreeReaderArray<double> myEnergy(myReader, "energy");
	TTreeReaderArray<double> numParticles(myReader, "nFinalParticles");
	TTreeReaderValue<int> myEvents(myReader, "iEvents");
	TTreeReaderValue<int> myNFinalParticles(myReader, "nFinalParticles");

	// vector<int> pTempV;
	vector<vector<int> > pIndex;
	//y is rapidity

	int	eventN = 0;
	int nJets = 0;


    //create output TTree
	TTree jetTree("jetTree", "ttree with jet data");
	jetTree.Branch("eventN", &eventN, "eventN/I");
	jetTree.Branch("nJets", &nJets, "nJets/I");
	jetTree.Branch("pIndex", &pIndex);

  //Pseudojet vector
  //vector of pseudoJets
	// vector<vector<PseudoJet>> particlesVector;
  //loop through the particles and turn them into pseudojets
	while(myReader.Next()) {
	//Note For Understanding: myReader.Next() --> iterates through the first level of the reader, or the only level for the value reader, the array reader needs to levels (understanding as of 6/20/17)

		vector<PseudoJet> particles;			
		for (int i = 0; i < *myNFinalParticles; i++)
		{
			PseudoJet pj(myPx[i], myPy[i], myPz[i], myEnergy[i]);
			pj.set_user_index(i);
			particles.push_back(pj);

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
			
			pIndex[i].push_back(jets[i].user_index());

			// pt.push_back(jets[i].pt());
			// phi.push_back(jets[i].phi());
			// y.push_back(jets[i].rap());
			// area.push_back(jets[i].area());

			// ptP.push_back(jets[i].constituents().pt())
			// phiP.push_back(jets[i].constituents().phi())
			// yP.push_back(jets[i].constituents().eta())

			// cout << "jet " << i << ": "<< jets[i].pt() << " " 
			// << jets[i].rap() << " " << jets[i].phi() << endl;
			// vector<PseudoJet> constituents = jets[i].constituents();
			// for (unsigned j = 0; j < constituents.size(); j++) {
			// 	cout << "    constituent " << j << "s pt: " << constituents[j].pt()      << endl;
		}
		nJets = jets.size();

		jetTree.Fill();

		eventN = eventN + 1;
			//}
	}
	jetTree.Print();
//write the tree to a file
	jetTree.Write();
	cout << "he";
//f.ls();
	a.Close();

	return 0;
		// particlesVector.push_back(particles);
} 

	// return 1;


	//resolution/code radius --.6

