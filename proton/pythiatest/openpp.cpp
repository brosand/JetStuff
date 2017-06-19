//use this to open the file and generate a histogram

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
void openpp(){
	
	//histogram
	TH1F *histogram = new TH1F("histogram", "histogram", 1000, -2, 2);
	//file
   	TFile *f = TFile::Open("ppfile.root");

	if (f == 0) {
	cout << "Error. Could not open file." << endl;
	return;
	}

	TCanvas canv("canvas", "canvas");
	canv.SetLogy();
	
	TTreeReader myReader("tree", f);
	TTreeReaderArray<double> myPx(myReader, "px");
	
	while(myReader.Next()){

		for(int i = 0, n = myPx.GetSize(); i < n; i++){
			histogram->Fill(myPx[i]);

		}
	}

	histogram->Draw();
	canv.SaveAs("px.pdf");

//return ;
}
