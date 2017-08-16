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
#include <string.h>
#ifdef __MAKECINT__
#pragma link C++ class std::vector<int> +;
#pragma link C++ class std::vector < std::vector<int> >+;   
#endif 


using namespace fastjet;
using namespace std;

int JET_ENERGY_LOWER_LIMIT=20;
// int JET_ENERGY_UPPER_LIMIT=50;
  // choose a jet definition
double R = 0.2;

int main (int argc, char * argv[]){
    //cout << argc << endl;
    string iPath, outputFolder;
    
    if (argc < 3){

        cout << "Error. Please enter only three command-line arguments. Aborting." << endl;
        exit;
    }

    if(argc < 1){
        cout << "Input file path: ";
        cin >> iPath;
        cout << "Input folder where you would like this jet tree to go: ";
        cin >> outputFolder;
    }

    iPath = argv[1];
    outputFolder = argv[2];
    R = atof(argv[3]);
    JET_ENERGY_LOWER_LIMIT = atof(argv[4]);


    string oPath;
    size_t pos = iPath.find(".");
    oPath = outputFolder +  "/" + iPath.substr(0, pos) + "Jet.root";

  //create a reader to interpret the TTree
    TFile *f = TFile::Open(iPath.c_str());
    TFile a(oPath.c_str(), "recreate");
    if (f == 0) {
        cout << "Error. Could not open file." << endl;
        return 1;
    }
    TTreeReader myReader("tree" ,f);
    TTreeReaderArray<double> myPx(myReader, "px");
    TTreeReaderArray<double> myPy(myReader, "py");
    TTreeReaderArray<double> myPz(myReader, "pz");
    TTreeReaderArray<double> myEnergy(myReader, "energy");
    // TTreeReaderArray<int> numParticles(myReader, "nFinalParticles"); //??
    // TTreeReaderValue<int> myEvents(myReader, "iEvents");
    TTreeReaderValue<int> myNFinalParticles(myReader, "nFinalParticles");

    // vector<int> pTempV;
    vector<vector<int> > pIndex;
    //y is rapidity

    int eventN = 0;
    int nJets = 0;
    vector<double> eta, phi, e;
    //create output TTree
    TTree jetTree("jetTree", "ttree with jet data");
    jetTree.Branch("eventN", &eventN, "eventN/I");
    jetTree.Branch("nJets", &nJets, "nJets/I");
    jetTree.Branch("pIndex", &pIndex);
    jetTree.Branch("phi", &phi);
    jetTree.Branch("eta", &eta);
    jetTree.Branch("e", &e);

  //Pseudojet vector
  //vector of pseudoJets
    // vector<vector<PseudoJet>> particlesVector;
  //loop through the particles and turn them into pseudojets
        // int iEvent = 0;
    while(myReader.Next()) {
    //Note For Understanding: myReader.Next() --> iterates through the first level of the reader, or the only level for the value reader, the array reader needs to levels (understanding as of 6/20/17)
        vector<PseudoJet> particles;            
        for (int i = 0; i < *myNFinalParticles; i++) //why pointer?
        {
            PseudoJet pj(myPx[i], myPy[i], myPz[i], myEnergy[i]);
            // cout << myEnergy[i] << endl;
            // cout << myPx[i] << endl;
            // cout << myEnergy[i] << endl;

            pj.set_user_index(i);
            particles.push_back(pj);
        // cout << "65" << endl;
        }

        JetDefinition jet_def(antikt_algorithm, R);
        AreaDefinition area_def(voronoi_area);
        // cout << "74" << endl;

// run the clustering, extract the jets
        ClusterSequenceArea cs(particles, jet_def, area_def);
        vector<PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());
        
        // cout << "Event number: " << iEvent << endl;
        // iEvent++;
//add the jet data to the final TTree

        //for each jet, loop through a single jet, adding each userindex to the array
        //jets.size is the number of jets
        for (int a = 0; a < jets.size(); a++) {
            // cout << jets[a].e() << endl;
            // if ((jets[a].e() < JET_ENERGY_LOWER_LIMIT)|| (jets[a].e() <  JET_ENERGY_UPPER_LIMIT)){
            if (jets[a].e() < JET_ENERGY_LOWER_LIMIT){

                jets.erase(jets.begin()+a);
                a--; //because it will a++ but we just moved the whole thing back, so we end up staying in same spot
            }
        }
        // cout << "jets.size is " << jets.size() << endl;

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
            e.push_back(jets[i].e());

//pIndex needs to increment outside, need to use pushback on it because pIndex at some i doesn't exist yet
          
        }
        nJets = jets.size();
        jetTree.Fill();
        if(eventN % 1000 == 0){
        cout << eventN << endl;
    }
        //cout << "102";
        eventN = eventN + 1;
        pIndex.clear();
        eta.clear();
        phi.clear();
        e.clear();
        pIndex.resize(0);
        eta.resize(0);
        phi.resize(0);
        e.resize(0);
            //}
    }

    jetTree.Write();
    jetTree.Print();
//write the tree to a file


//f.ls();
    a.Close();

    return 0;
} 




