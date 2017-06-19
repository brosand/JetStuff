//create a lead-lead collision

//run name in Makefile is pbtree

#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <TF1.h>
#include "TTree.h"
#include "TH1.h"
#include "TFile.h"
#include "TMath.h"

//test1
using namespace std;

int main(){

	int iEvents, nEvents, iParticles, nParticles;
	
	double tao, pt, px, py, pz, theta, phi, eta;
        srand(time(NULL));
	/*partdata
	struct particle_STRUCT {

		Double_t pt, px, py, pz
		//later I can make this an array, or use lorentz vector			
	};*/
	
	cout << "Enter the number of events: ";
        cin >> nEvents;

        cout << "Enter the number of particles per event: ";
        cin >> nParticles;

	//create an array of structures
	//partdata particle_STRUCT particleStructArray[nParticles];

	//create a tree and link it
	TTree tree("tree", "tree with 2 ints and a struct");
	tree.Branch("iEvents", &iEvents, "iEvents/I");
	tree.Branch("nParticles", &nParticles, "nParticles/I");
	//partdata tree.Branch("Particle_info", &someParticle, "EventNo/I:NoParticles/I:partInfo[nParticles]/particle_STRUCT");

        //cout << "Enter the time constant: ";
        //cin >> tao;

	TF1 *expdec = new TF1("expdec", "exp(-x/300)", 0, 1000000); 
	//expdec->SetParameter(tao);

	cout << "\tParticle No.\tp_t\t\tp_x\t\tp_y\t\tp_z\t\t" << endl;
	
	for(iEvents = 0; iEvents < nEvents; iEvents++){
	
		cout << "\nEvent " << iEvents << "\n" << endl;
/*partdata
		//loop for particles
		for(iParticles = 0; iParticles < nParticles; iParticles++){
			
		//cout << "Hello" << endl;
				
		        //get a random pt from the exp decay distribution
		        particleStructArray[i].pt = expdec -> GetRandom();
		        phi = rand()/double(RAND_MAX)*2.0*M_PI;

		        //from phi what are px and py
		        particleStructArray[i].px = particleStructArray[i].pt*cos(phi);
	 		particleStructArray[i].py = particleStructArray[i].pt*sin(phi);

		        //what is eta (psuedorapidity)
		        eta = ((rand()/double(RAND_MAX))*2.0) - 1;
			
			//theta
			theta = 2.0*atan(exp(-eta));

			//pz
			particleStructArray[i].pz = particleStructArray[i].pt/(tan(theta));	
			
			cout << "\t\t" << iParticles << "\t" << pt << "\t\t" << px << "\t\t" << py << "\t\t" << pz << endl;

		}*/
	tree.Fill();	

	} 

//print the tree
tree.Print();

//write the tree to a file
TFile f("pbfile.root", "recreate");
tree.Write();
//f.ls();
f.Close();

return 0;
}



