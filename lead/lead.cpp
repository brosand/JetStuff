//create a lead-lead collision

#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <TF1.h>


using namespace std;

int main(){

	int nEvents, nParticles;
	
	double tao, pt, px, py, pz, theta, phi, eta;
        srand(time(NULL));
	
	cout << "Enter the number of events: ";
        cin >> nEvents;

        cout << "Enter the number of particles per event: ";
        cin >> nParticles;

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
		        pt = expdec -> GetRandom();
		        phi = rand()/double(RAND_MAX)*2.0*M_PI;

		        //from phi what are px and py
		        px = pt*cos(phi);
	 		py = pt*sin(phi);

		        //what is eta (psuedorapidity)
		        eta = ((rand()/double(RAND_MAX))*2.0) - 1;
			
			//theta
			theta = 2.0*atan(exp(-eta));

			//pz
			pz = pt/(tan(theta));	
			
			cout << "\t\t" << iParticles << "\t" << pt << "\t\t" << px << "\t\t" << py << "\t\t" << pz << endl;

		}

	}
return 0;
}



