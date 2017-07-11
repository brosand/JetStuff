//create a lead-lead collision

//run name in Makefile is pbtree
//now just make an array for all the px, all the py, etc. Many branches that all contain the same variable, the index tells what particle it is
#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <TF1.h>
#include "TTree.h"
#include "TH1.h"
#include "TFile.h"
#include "TMath.h"
#include "TRandom.h"


using namespace std;

int main(){

	int iEvents, nEvents, iParticles, nFinalParticles, chargetemp;
	
	double tao, theta, phi, eta;
        srand(time(NULL));
	
	cout << "Enter the number of events: ";
        cin >> nEvents;

        cout << "Enter the number of particles per event: ";
        cin >> nFinalParticles;

	double pt[nFinalParticles], px[nFinalParticles], py[nFinalParticles], pz[nFinalParticles], mass[nFinalParticles], energy[nFinalParticles];
	int charge[nFinalParticles];

	//create a tree and link it
	TTree tree("tree", "tree with event data and particle data in arrays");
	tree.Branch("iEvents", &iEvents, "iEvents/I");
	tree.Branch("nFinalParticles", &nFinalParticles, "nFinalParticles/I");
	tree.Branch("pt", &pt, "pt[nFinalParticles]/D");
	tree.Branch("px", &px, "px[nFinalParticles]/D");
	tree.Branch("py", &py, "py[nFinalParticles]/D");
	tree.Branch("pz", &pz, "pz[nFinalParticles]/D");
	tree.Branch("charge", &charge, "charge[nFinalParticles]/I");
	tree.Branch("mass", &mass, "mass[nFinalParticles]/D");
	tree.Branch("energy", &energy, "energy[nFinalParticles]/D");

        //cout << "Enter the time constant: ";
        //cin >> tao;

	//TF1 *expdec = new TF1("expdec", "10.0*exp(-x/0.3)", 0, 200); 
		
	//expdec->SetParameter(tao);
	TRandom * myRand = new TRandom();

	cout << "\tParticle No.\tp_t\t\tp_x\t\tp_y\t\tp_z\t\t" << endl;
	
	for(iEvents = 0; iEvents < nEvents; iEvents++){
	
		cout << "\nEvent " << iEvents << "\n" << endl;

		//loop for particles
		for(iParticles = 0; iParticles < nFinalParticles; iParticles++){
			
		//cout << "Hello" << endl;
				
		        //get a random pt from the exp decay distribution
		        //pt[iParticles] = expdec -> GetRandom(0.0, 200.0);			
			pt[iParticles] = myRand->Exp(0.3);

		        phi = rand()/double(RAND_MAX)*2.0*M_PI;

		        //from pt and phi what are px and py
		        px[iParticles] = pt[iParticles]*cos(phi);
	 		py[iParticles] = pt[iParticles]*sin(phi);

		        //what is eta (psuedorapidity)
		        eta = ((rand()/double(RAND_MAX))*2.0) - 1;
			
			//theta
			theta = 2.0*atan(exp(-eta));

			//pz
			pz[iParticles] = pt[iParticles]/(tan(theta));		
			//mass
			mass[iParticles] = 0.139570; //pion

			//energy
			energy[iParticles] = sqrt(pow(pt[iParticles], 2)+pow(pt[iParticles], 2)+pow(pt[iParticles], 2));	

			//charge	
			chargetemp = (rand()/double(RAND_MAX))*3;
	
			if((chargetemp >= 0) && (chargetemp < 1)){

				charge[iParticles] = -1;			
	
			} else if ((chargetemp >= 1) && (chargetemp < 2)){

				charge[iParticles] = 0;			
	
			} else if ((chargetemp >= 2) && (chargetemp < 3)){

				charge[iParticles] = 1;			
	
			} 			


			cout << "\t\t" << iParticles << "\t" << pt[iParticles] << "\t\t" << px[iParticles] << "\t\t" << py[iParticles] << "\t\t" << pz[iParticles] << "\t\t"<< charge[iParticles] << endl;

		}//loop for particles

	tree.Fill();	

	} 

//print the tree
tree.Print();

//write the tree to a file
TFile f("lead.root", "recreate");
tree.Write();
//f.ls();
f.Close();

return 0;
}



