//macro to open up the .root file

#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <cmath>
#include <time.h>

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TH1.h"

#include "TTreeReader.h"
//#include "TTreeReaderValue.h"
#include <TTreeReaderArray.h>

using namespace std;
//int main(){
void openpb(){
	
	//histogram
	TH1F *histogram = new TH1F("histogram", "histogram", 1000, 0, 10000);
	//file
   	TFile *f = TFile::Open("pbfile.root");

	if (f == 0) {
	cout << "Error. Could not open file." << endl;
	return;
	}
	
	//old way
	//TTree *mytree = (TTree *) f->Get("tree");
	//mytree->SetMarkerColor(7);
	//mytree->Draw("pt>>histogram");

	//new way
	TCanvas canv("canvas", "canvas");
	canv.SetLogy();
	
	//tree reader
	TTreeReader myReader("tree", f);
	TTreeReaderArray<double> myPt(myReader, "pt");
	
	while(myReader.Next()){

		for(int i = 0, n = myPt.GetSize(); i < n; i++){
			histogram->Fill(myPt[i]);

		}
	}
	
	/*
	for(iEvents = 0; iEvents < nEvents; iEvents++){

			for(iParticles = 0; iParticles < nParticles; iParticles++){

				histogram->Fill(*myPt);

			}
	}*/

	histogram->Draw();
	canv.SaveAs("pt.pdf");

//return ;
}
