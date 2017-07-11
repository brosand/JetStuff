#include "fastjet/ClusterSequenceArea.hh"

/*
/home/yu.yale.edu/br384/fastjet-3.2.2/include/fastjet/ClusterSequenceArea.hh
/home/yu.yale.edu/br384/fastjet-install/include/fastjet/ClusterSequenceArea.hh
*/

#include "fastjet/PseudoJet.hh"
#include <iostream>
#include <stdlib.h>

#include <TF1.h>
#include "TTree.h"
#include "TFile.h"
#include "TTreeReader.h"
#include <TTreeReaderArray.h>
/*#include <vector>
#ifdef __MAKECINT__
#pragma link C++ class std::vector < std::vector<int> >+;   
#endif */


using namespace fastjet;
using namespace std;

int main (){
	
	
  // cout << "test1";
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
	TTreeReaderArray<double> numParticles(myReader, "nFinalParticles");
	TTreeReaderValue<int> myEvents(myReader, "iEvents");
	TTreeReaderValue<int> myNFinalParticles(myReader, "nFinalParticles");

	// vector<int> pTempV;
	vector<vector<int> > pIndex;
	//y is rapidity

	int eventN = 0;
	int nJets = 0;
	vector<double> y, phi;


    //create output TTree
	TTree jetTree("jetTree", "ttree with jet data");
	jetTree.Branch("eventN", &eventN, "eventN/I");
	jetTree.Branch("nJets", &nJets, "nJets/I");
	jetTree.Branch("pIndex", &pIndex);
	jetTree.Branch("phi", &phi);
	jetTree.Branch("y", &y);

  //Pseudojet vector
  //vector of pseudoJets
	// vector<vector<PseudoJet>> particlesVector;
  //loop through the particles and turn them into pseudojets
	while(myReader.Next()) {
	//Note For Understanding: myReader.Next() --> iterates through the first level of the reader, or the only level for the value reader, the array reader needs to levels (understanding as of 6/20/17)
		// cout << "58";
		vector<PseudoJet> particles;			
		for (int i = 0; i < *myNFinalParticles; i++)
		{
			PseudoJet pj(myPx[i], myPy[i], myPz[i], myEnergy[i]);
			pj.set_user_index(i);
			particles.push_back(pj);
		// cout << "65" << endl;
		}


  		// choose a jet definition
		double R = 0.6;

		JetDefinition jet_def(antikt_algorithm, R);
		AreaDefinition area_def(voronoi_area);
		// cout << "74" << endl;
  
// run the clustering, extract the jets
		ClusterSequenceArea cs(particles, jet_def, area_def);
		vector<PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());
  
//add the jet data to the final TTree
		// cout << "79";

		//loop through a single jet, adding each userindex to the array
		for (int i = 0; i < jets.size(); i++) {
			vector<int> pTempV;
			for (int b = 0; b < jets[i].constituents().size(); b++){			

				pTempV.push_back(jets[i].user_index());
				cout << pTempV[b] << endl;

			}

			cout << "break" << endl;	

			pIndex.push_back(pTempV);
			//cout << pIndex[i] << endl;
			phi.push_back(jets[i].phi());
			y.push_back(jets[i].rap());

//pIndex needs to increment outside, need to use pushback on it because pIndex at some i doesn't exist yet
			// pt.push_back(jets[i].pt());
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
		//cout << "102";
		eventN = eventN + 1;
			//}
	}

	//cout << "index 4 2: " << pIndex.at(4,2) << endl;
	//cout << "index 3 5: " << pIndex.at(3,5) << endl;
	cout << "index 7 1: " << pIndex[7][1] << endl;
	cout << "index 12 11: " << pIndex[12][11] << endl;

	jetTree.Print();
//write the tree to a file
	TFile a("jetFile.root", "recreate");
	jetTree.Write();

//f.ls();
	a.Close();

	return 0;
		// particlesVector.push_back(particles);
} 

	// return 1;


	//resolution/code radius --.6

