//macro to open up the .root file
//now this one is a .c

#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <time.h>

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"

using namespace std;
//int main(){
void openpb(){

   	TFile *f = TFile::Open("pbfile.root");

	if (f == 0) {
	cout << "Error. Could not open file." << endl;
	return;
	}

	TTree *mytree = (TTree *) f->Get("tree");
	//mytree->SetMarkerColor(7);
	mytree->Draw("iEvent:nParticles");
	//could just do sphere.Draw(---) but that is less elegant

return ;
}
