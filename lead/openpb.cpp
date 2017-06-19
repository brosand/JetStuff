//macro to open up the .root file

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
	mytree->Draw("iEvents");


//return ;
}
