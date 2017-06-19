//create a lead-lead collision, and put this info into a tree

#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <TF1.h>


using namespace std;

int main(){

	int nEvents, nParticles;
	
	double tao, pt, px, py, pz, theta;
        srand(time(NULL));

	struct particle_STRUCT {

		Double_t pt, px, py, pz
		//later I can make this an array, or use lorentz vector			
	};
	
	cout << "Enter the number of events: ";
        cin >> nEvents;

        cout << "Enter the number of particles per event: ";
        cin >> nParticles;

	//create an array of structures
	particle_STRUCT particleStructArray[nParticles];

	//create a tree and link it
	TTree tree("tree", "tree with 2 ints and a struct");
	tree.Branch("Particle_info", &someParticle, "EventNo/I:NoParticles/I:partInfo[nParticles]/particle_STRUCT");

        //cout << "Enter the time constant: ";
        //cin >> tao;

	TF1 *expdec = new TF1("expdec", "exp(-x/300)", 0, 1000000); 
	//expdec->SetParameter(tao);

	cout << "\tParticle No.\tp_t\t\tp_x\t\tp_y\t\tp_z\t\t" << endl;

	for(int iEvents = 0; iEvents < nEvents; iEvents++){
	
		cout << "\nEvent " << iEvents << "\n" << endl;

		//loop for particles
		for(int iParticles = 0; iParticles < nParticles; iParticles++){
			
		//cout << "Hello" << endl;
				
		        //get a random pt from the exp decay distribution
		        particleStructArray[i].pt = expdec -> GetRandom();
		        theta = rand()/double(RAND_MAX)*2.0*M_PI;

		        //from theta what are px and py
		        particleStructArray[i].px = particleStructArray[i].pt*cos(theta);
	 		particleStructArray[i].py = particleStructArray[i].pt*sin(theta);

		        //what is pz
		        particleStructArray[i].pz = (rand()/double(RAND_MAX)*2.0) - 1;
			cout << "\t\t" << iParticles << "\t" << particleStructArray.pt << "\t\t" << particleStructArray[i].px << "\t\t" << particleStructArray[i].py << "\t\t" << particleStructArray[i].pz << endl;

		}

	}
return 0;
}



