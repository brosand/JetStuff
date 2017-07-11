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
#include <vector>
#ifdef __MAKECINT__
#pragma link C++ class std::vector<int> +;
#pragma link C++ class std::vector < std::vector<int> >+;   
#endif 


using namespace fastjet;
using namespace std;

int JET_ENERGY_LOWER_LIMIT=20;

int main (){
	string oPath, iPath;

	cout << "Input file path: ";
	cin >> iPath;

	cout << "Input output file path:";
	cin >> oPath;
  // cout << "test1";
  //create a reader to interpret the TTree
	TFile *f = TFile::Open(iPath.c_str());
	cout << "hi" <<iPath.c_str();	
	TFile a("pbJet.root", "recreate");
	if (f == 0) {
		cout << "Error. Could not open file." << endl;
		return 1;
	}

	TTreeReader myReader("tree" ,f);
	TTreeReaderArray<double> myPx(myReader, "px");
	TTreeReaderArray<double> myPy(myReader, "py");
	TTreeReaderArray<double> myPz(myReader, "pz");
	TTreeReaderArray<double> myEnergy(myReader, "energy");
	TTreeReaderArray<int> numParticles(myReader, "nFinalParticles"); //??
	// TTreeReaderValue<int> myEvents(myReader, "iEvents");
	TTreeReaderValue<int> myNFinalParticles(myReader, "nFinalParticles");

	// vector<int> pTempV;
	vector<vector<int> > pIndex;
	//y is rapidity

	int eventN = 0;
	int nJets = 0;
	vector<double> eta, phi;


    //create output TTree
	TTree jetTree("jetTree", "ttree with jet data");
	jetTree.Branch("eventN", &eventN, "eventN/I");
	jetTree.Branch("nJets", &nJets, "nJets/I");
	jetTree.Branch("pIndex", &pIndex);
	jetTree.Branch("phi", &phi);
	jetTree.Branch("eta", &eta);

  //Pseudojet vector
  //vector of pseudoJets
	// vector<vector<PseudoJet>> particlesVector;
  //loop through the particles and turn them into pseudojets
        // int iEvent = 0;
	while(myReader.Next()) {
	//Note For Understanding: myReader.Next() --> iterates through the first level of the reader, or the only level for the value reader, the array reader needs to levels (understanding as of 6/20/17)
		cout << "num particles in this jet is " << *myNFinalParticles << endl;
		cout << "test";
		vector<PseudoJet> particles;			
		for (int i = 0; i < *myNFinalParticles; i++) //why pointer?
		{
			PseudoJet pj(myPx[i], myPy[i], myPz[i], myEnergy[i]);
			cout << myEnergy[i];
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
		
		// cout << "Event number: " << iEvent << endl;
		// iEvent++;
//add the jet data to the final TTree
		// cout << "79";

		//for each jet, loop through a single jet, adding each userindex to the array
		//jets.size is the number of jets
		for (int a = 0; a < jets.size(); a++) {
			cout << jets[a].pt() << endl;
			if (jets[a].pt() < JET_ENERGY_LOWER_LIMIT) {
				jets.erase(jets.begin()+a);
				a--;
			}
		}
		cout << "jets.size is " << jets.size() << endl;

		//jets[i].constituents().size() is the number of particles in that jet
		for (int i = 0; i < jets.size(); i++) {
			vector<int> pTempV;
			// cout << "\tjets[" << i << "].constituents().size() is " << jets[i].constituents().size() << endl;
			for (int b = 0; b < jets[i].constituents().size(); b++){
				//constituents=jets[i].constituents();			
				// cout << "\t\tjets[" << i << "]user_index: " << jets[i].constituents()[b].user_index() << endl;
				// a = pIndex[i].push_back(0);
				pTempV.push_back(jets[i].constituents()[b].user_index()); //Michael imp
				//cout << pTempV[b] << endl;
				// cout << "test" << endl;

			}

			//cout << "break" << endl;	

			pIndex.push_back(pTempV);
			pTempV.clear();
			pTempV.resize(0);
			// cout << pTempV[0] << endl;
			// cout << pIndex[0][0] << endl;
			phi.push_back(jets[i].phi());
			eta.push_back(jets[i].rap());

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
		pIndex.clear();
		eta.clear();
		phi.clear();
		pIndex.resize(0);
		eta.resize(0);
		phi.resize(0);

			//}
	}

	jetTree.Write();
	jetTree.Print();
//write the tree to a file


//f.ls();
	a.Close();

	return 0;
		// particlesVector.push_back(particles);
} 

	// return 1;


	//resolution/code radius --.6

