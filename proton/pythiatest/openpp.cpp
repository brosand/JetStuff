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
#include "TTreeReaderValue.h"
#include <TTreeReaderArray.h>

using namespace std;
//int main(){
void openpp(){
	
	//histogram for number of final particles
	TH1F *histogramnFP = new TH1F("histogramnFP", "histogramnFP", 40, 0, 200);
	//histogram for px
	TH1F *histogrampx = new TH1F("histogrampx", "histogrampx", 40, 0, 1);
	TH1F *histogrampy = new TH1F("histogrampy", "histogrampy", 40, 0, 1);
	TH1F *histogrampz = new TH1F("histogrampz", "histogrampz", 40, 0, 1);
	TH1F *histograme = new TH1F("histograme", "histograme", 40, 0, 200);
	TH1F *histogramcharge = new TH1F("histogramcharge", "histogramcharge", 5, -2, 2);
	TH1F *histogrammass = new TH1F("histogrammass", "histogrammass", 100, 0, 1);
	//file
   	TFile *f = TFile::Open("ppfile.root");

	if (f == 0) {
	cout << "Error. Could not open file." << endl;
	return;
	}

	TCanvas cnFP("cnFP", "cnFP");
	TCanvas cpx("cpx", "cpx");
	cpx.SetLogy();
	TCanvas cpy("cpy", "cpy");
	cpy.SetLogy();
	TCanvas cpz("cpz", "cpz");
	cpz.SetLogy();
	TCanvas ccharge("ccharge", "ccharge");
	TCanvas cenergy("cenergy", "cenergy");
	cenergy.SetLogy();
	TCanvas cmass("cmass", "cmass");

	
	TTreeReader myReader("tree", f);
	TTreeReaderValue<int> mynFinalParticles(myReader, "nFinalParticles");
	TTreeReaderArray<double> myPx(myReader, "px");
	TTreeReaderArray<double> myPy(myReader, "py");
	TTreeReaderArray<double> myPz(myReader, "pz");
	TTreeReaderArray<double> myEnergy(myReader, "energy");
	TTreeReaderArray<int> myCharge(myReader, "charge");
	TTreeReaderArray<double> myMass(myReader, "mass");

	while(myReader.Next()){
		
		histogramnFP->Fill(*mynFinalParticles);

		for(int i = 0, n = myPx.GetSize(); i < n; i++){
			histogrampx->Fill(myPx[i]);
			histogrampy->Fill(myPy[i]);
			histogrampz->Fill(myPz[i]);
			histograme->Fill(myEnergy[i]);
			histogramcharge->Fill(myCharge[i]);
			histogrammass->Fill(myMass[i]);

		}
	}

	cnFP.cd();
		histogramnFP->Draw();
	cpx.cd();	
		histogrampx->Draw();
	cpy.cd();
		histogrampy->Draw();
	cpz.cd();
		histogrampz->Draw();
	cenergy.cd();
		histograme->Draw();
	ccharge.cd();
		histogramcharge->Draw();
	cmass.cd();
		histogrammass->Draw();

	cnFP.SaveAs("nFinalParticles.pdf");
	cpx.SaveAs("px.pdf");
	cpy.SaveAs("py.pdf");
	cpz.SaveAs("pz.pdf");
	cenergy.SaveAs("energy.pdf");
	ccharge.SaveAs("charge.pdf");
	cmass.SaveAs("mass.pdf");


//return ;
}
