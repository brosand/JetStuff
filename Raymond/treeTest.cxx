// Test tree functionality in python

#include <TFile.h>
#include <TTree.h>

void treeTest()
{
  TFile * fIn = TFile::Open("treeTest.root", "RECREATE");

  TTree tree("treeTest", "Tree Test");

  int testVal = 0;

  tree.Branch("testVal", &testVal);

  for (int i = 0; i < 10; i++)
  {
    testVal = i;
    tree.Fill();
  }

  fIn->Write();
  fIn->Close();
}

int main(int argc, char * argv[])
{
  treeTest();

  return 0;
}
