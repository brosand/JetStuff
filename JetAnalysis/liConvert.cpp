//the purpose of this is to take Kirill's raw data and turn it into a tree that matches the trees that we have already made

// #include <iostream>
// #include <iomanip>
#include <stdlib.h>
#include "TTree.h"
#include "TFile.h"
#include "TMath.h"
#include "TTreeReader.h"
#include <TTreeReaderArray.h>
#include <vector>
#include <fstream>
#include <string>
#include <string.h>
#include <cstring>
#include "optionparser.h"
// namespace po = boost::program_options;
using namespace std;
// using namespace po;
int main(int argc, char * argv[]){

	string iPath, outputFolder;
      if (argc > 3){

        cout << "Error. Please enter only two command-line arguments. Aborting." << endl;
        exit;
    }

    iPath = argv[1];
    outputFolder = argv[2];
    if(argc < 1){
        cout << "Input file path: ";
        cin >> iPath;
        cout << "Input folder where you would like this jet tree to go: ";
        cin >> outputFolder;
    }
    // iPath = "";
    // for(int i = 0; i < sizeof(argv[1][0]); i++)
    // {
    	// iPath.append(&argv[1][i]);
    // }
    // cout << iPath;

    TFile *f = TFile::Open(iPath.c_str());
    TTreeReader myReader("JetTree" ,f);
    TTreeReaderArray<float> myPx(myReader, "fPrimaryTracks.fPx");
    TTreeReaderArray<float> myPy(myReader, "fPrimaryTracks.fPy");
    TTreeReaderArray<float> myPz(myReader, "fPrimaryTracks.fPz");

	int nFinalParticles; 
	vector <double> px;
	vector <double> py;
	vector <double> pz;
	vector <double> energy;
	string filename, rootFileName, waste;
    
    string oPath;
    size_t pos = iPath.find(".");
    oPath = outputFolder +  "/" + iPath.substr(0, pos) + "C.root";

	rootFileName = oPath;
	TFile *a = new TFile(rootFileName.c_str(), "recreate");
//create a tree and link it
	TTree tree("tree", "tree with event data and particle data in arrays");
	tree.Branch("nFinalParticles", &nFinalParticles);
	tree.Branch("px", &px);
	tree.Branch("py", &py);
	tree.Branch("pz", &pz);
	tree.Branch("energy", &energy);


	// cout << "Enter the name of the file to read from (probs a .dat):\t";
	// cin >> filename;

	// rootFileName = filenam 	e.substr(0, pos) + ".root";

	while(myReader.Next()) {
		int ctr = 0;
		for (int i = 0; i < myPx.GetSize(); i++){
			px.push_back(float(myPx[i]));
			py.push_back(float(myPy[i]));
			pz.push_back(float(myPz[i]));
			nFinalParticles = myPx.GetSize();
			energy.push_back(pow((pow(myPx[i],2))+(pow(myPy[i],2))+(pow(myPz[i],2)),.5));
			ctr++;

		}
		tree.Fill();
		px.clear();
		py.clear();
		pz.clear();
		energy.clear();

}
	tree.Write();

	tree.Print();
	//f.ls();

	a->Close();


}

