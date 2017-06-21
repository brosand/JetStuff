#!/usr/bin/env python

import ROOT
import array

def createTree(filename):
    fOut = ROOT.TFile(filename, "RECREATE")

    # See: The corresponding .cxx
    # See: https://root.cern.ch/how/how-write-ttree-python

def readTree(filename):
    fIn = ROOT.TFile(filename, "READ")

    tree = fIn.Get("treeTest")

    hist = ROOT.TH1F("hist", "hist", 10, 0, 10)

    for i, event in enumerate(tree):
        print("{0}: {1}".format(i, event.testVal))
        hist.Fill(event.testVal)

    canvas = ROOT.TCanvas("canvas", "canvas")
    hist.Draw()
    canvas.SaveAs("testHist.pdf")

# This is like main(). It will execute every time
if __name__ == "__main__":
    filename = "treeTest.root"
    #createTree(filename = filename)

    readTree(filename = filename)
