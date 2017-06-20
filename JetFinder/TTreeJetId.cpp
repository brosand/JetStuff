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

	double mPion = 139.570;

  //create a reader to interpret the TTree
	TFile *f = TFile::Open("pbfile.root");	
	
	if (f == 0) {
		cout << "Error. Could not open file." << endl;
		return 1;
	}

	TTreeReader myReader("tree" ,f);
	TTreeReaderArray<double> myPx(myReader, "px");
	TTreeReaderArray<double> myPy(myReader, "py");
	TTreeReaderArray<double> myPz(myReader, "pz");


  // //loop through the Ttree TTree
  // while(myReader.Next()){
  // 	for (int i = 0; n = myPt.GetSize(); i < n; i++) {

  // 	}`
  // }

  //loop through the particles and turn them into pseudojets
	vector<PseudoJet> particles;
	while(myReader.Next()) {
		for (int i = 0; i < myPx.GetSize(); i++)
		{
			particles.push_back(PseudoJet(myPx[i], myPy[i], myPz[i], mPion));
		}
	}
  // an event with three particles:   px    py  pz      E
  //particles.push_back( PseudoJet(   99.0,  0.1,  0, 100.0) ); 
  //particles.push_back( PseudoJet(    4.0, -0.1,  0,   5.0) ); 
  //particles.push_back( PseudoJet(  -99.0,    0,  0,  99.0) );

  // choose a jet definition
	double R = 0.7;
	JetDefinition jet_def(antikt_algorithm, R);
	cout << "test3"<< endl;
  // run the clustering, extract the jets
	ClusterSequence cs(particles, jet_def);
	vector<PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());

  // print out some infos
	cout << "Clustering with " << jet_def.description() << endl;

  // print the jets
	cout <<   "        pt y phi" << endl;
	for (unsigned i = 0; i < jets.size(); i++) {
		cout << "jet " << i << ": "<< jets[i].pt() << " " 
		<< jets[i].rap() << " " << jets[i].phi() << endl;
		vector<PseudoJet> constituents = jets[i].constituents();
		for (unsigned j = 0; j < constituents.size(); j++) {
			cout << "    constituent " << j << "'s pt: " << constituents[j].pt()      << endl;
		}
	}
} 
