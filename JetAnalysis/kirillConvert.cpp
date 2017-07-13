//the purpose of this is to take Kirill's raw data and turn it into a tree that matches the trees that we have already made

#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include "TTree.h"
#include "TFile.h"
#include "TMath.h"
#include <vector>
#include <fstream>
#include <string>
#include <string.h>
#include <cstring>
using namespace std;

int main(){

	int dummy, iEvents = 0;

	vector <int> nFinalParticles; //technically not final any more, but for naming consistency
	vector <double> px;
	vector <double> py;
	vector <double> pz;
	vector <double> energy;
	vector <double> mass;

//create a tree and link it
	TTree tree("tree", "tree with event data and particle data in arrays");
	tree.Branch("iEvents", &iEvents, "iEvents/I");
	tree.Branch("nFinalParticles", &nFinalParticles);
	tree.Branch("px", &px);
	tree.Branch("py", &py);
	tree.Branch("pz", &pz);
	tree.Branch("energy", &energy);
	tree.Branch("mass", &mass);

	cout << "seg1" << endl;

	ifstream inputFile;
	string filename, rootFileName, waste;

	cout << "Enter the name of the file to read from (a .dat probs):\t";
	cin >> filename;

	inputFile.open(filename);

	if(inputFile.fail()){

        	cout << "Error: The file named " << filename << " was not successfully opened." << endl;

	}
	cout << "seg2" << endl;

	iEvents = 0;
	for(int j = 0; j < 3; j++){

		getline(inputFile, waste);
		//cout << "ignore " << j << endl;	

		}

	while(!inputFile.eof()){

		int nFinalParticlesTemp;
		inputFile >> iEvents >> nFinalParticlesTemp >> dummy >> dummy; //in top line
		nFinalParticles.push_back(nFinalParticlesTemp);
		//cout << "yo2"  << endl;
		cout << "iEvents: "<< iEvents << endl;

		for (int i = 0; i < nFinalParticles[iEvents]; i++){ 
				// particle number, particle id aren't needed
			
			cout << "i " << i << endl;
			int dummy, pxtemp, pytemp, pztemp, energytemp, masstemp;
			inputFile >> dummy >> dummy >> pxtemp >> pytemp >> pztemp >> energytemp >> masstemp >> dummy >> dummy;

			//fill vectors
			px.push_back(pxtemp);
			py.push_back(pytemp);
			pz.push_back(pztemp);
			energy.push_back(energytemp);
			mass.push_back(masstemp);
			
			//cout << iEvents << "\t" << i << "\t" << px.at(nFinalParticles) << "\t" << py.at(nFinalParticles) << "\t" << pz.at(nFinalParticles) << "\t" << energy.at(nFinalParticles) << "\t" << "\t" << mass.at(nFinalParticles) << endl;
			
		}

		tree.Fill();
		px.clear();
		py.clear();
		pz.clear();
		energy.clear();
		mass.clear();
	
		//iEvents++;


	}
	cout << "seg3" << endl;	
	
	tree.Print();

	size_t pos = filename.find(".");
	  //std::string str3 = str.substr (pos);     // get from "live" to the end
    	rootFileName = filename.substr(0, pos);

	TFile *f = new TFile(rootFileName.c_str(), "recreate");
	tree.Write();
	//f.ls();
	f->Close();

	return 0;

}

