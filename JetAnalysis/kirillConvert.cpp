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

	int dummyI, iEvents = 0, nFinalParticlesTemp;
	double dummyD;
	double pxtemp, pytemp, pztemp, energytemp, masstemp;
	int nFinalParticles; //technically not final any more, but for naming consistency
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

	ifstream inputFile;
	string filename, rootFileName, waste;

	cout << "Enter the name of the file to read from (probs a .dat):\t";
	cin >> filename;

	inputFile.open(filename);
	

	if(inputFile.fail()){

		cout << "Error: The file named " << filename << " was not successfully opened." << endl;

	}

	size_t pos = filename.find(".");
	rootFileName = filename.substr(0, pos) + ".root";
	TFile *f = new TFile(rootFileName.c_str(), "recreate");

	iEvents = 0;
	for(int j = 0; j < 3; j++){

		getline(inputFile, waste);

	}

	while(inputFile >> iEvents >> nFinalParticles >> dummyD >> dummyD){

		if (iEvents % 100 == 0){
			cout << "iEvents: "<< iEvents << " nFinalParticles: " << nFinalParticles << endl;
		}

		for (int i = 0; i < nFinalParticles; i++){ 
				// particle number, particle id aren't needed
			
			inputFile >> dummyI >> dummyI >> pxtemp >> pytemp >> pztemp >> energytemp >> masstemp >> dummyD >> dummyD >> dummyD >> dummyD;

			//fill vectors
			px.push_back(pxtemp);
			py.push_back(pytemp);
			pz.push_back(pztemp);
			energy.push_back(energytemp);
			mass.push_back(masstemp);

			//cout << "\t\t" << i << "\t" << pxtemp << "\t" << pytemp << "\t" << pztemp << "\t" << energytemp << "\t" << masstemp << "\t" << endl;
			
			// cout << "\t\t" << i << "\t" << px.at(i) << "\t" << py.at(i) << "\t" << pz.at(i) << "\t" << energy.at(i) << "\t" << mass.at(i) << endl;
		}
		tree.Fill();

		px.clear();
		py.clear();
		pz.clear();
		energy.clear();
		mass.clear();

		//iEvents++;
	}

	tree.Write();

	tree.Print();
	//f.ls();

	f->Close();

	return 0;

}

