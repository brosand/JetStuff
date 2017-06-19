#include "fastjet/ClusterSequence.hh"
#include <iostream>
using namespace fastjet;
using namespace std;

int main () {

	double mPion = 139.570

  //create a reader to interpret the TTree
  TFile *f = TFile::Open("pbfile.root");
  TTreeReader myReader("tree", f);
  TTreeReeaderArray<double> myPx(myReader, "px");
  TTreeReeaderArray<double> myPy(myReader, "py");
  TTreeReeaderArray<double> myPz(myReader, "pz");

  // //loop through the Ttree TTree
  // while(myReader.Next()){
  // 	for (int i = 0; n = myPt.GetSize(); i < n; i++) {

  // 	}
  // }

  //loop through the particles and turn them into pseudojets
  vector<PseudoJet> particles;
  for (int i = 0; i < myPx.GetSize(); i++)
  {
  	particles.push_back(PseudoJet(myPx[i], myPy[i], myPz[i], mPion));
  }
  // an event with three particles:   px    py  pz      E
  particles.push_back( PseudoJet(   99.0,  0.1,  0, 100.0) ); 
  particles.push_back( PseudoJet(    4.0, -0.1,  0,   5.0) ); 
  particles.push_back( PseudoJet(  -99.0,    0,  0,  99.0) );

  // choose a jet definition
  double R = 0.7;
  JetDefinition jet_def(antikt_algorithm, R);

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
      cout << "    constituent " << j << "'s pt: " << constituents[j].pt()
           << endl;
    }
  }
} 
