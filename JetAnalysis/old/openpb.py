#macro to open up the .root file
#NOW IN PYTHON


#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <time.h>

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TH1.h"

#int main(){
def openpb():

   	TFile *f = TFile::Open("pbfile.root");

	if (f == 0):
		cout << "Error. Could not open file." << endl;
		return;
	
	TH1F *histogram = new TH1F("histogram", "histogram", 100, -0.0001, 0.0001);

	TTree *mytree = (TTree *) f->Get("tree");

	mytree->Draw("px>>histogram");


	#return ;

