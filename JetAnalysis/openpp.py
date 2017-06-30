#translate openpp.cpp to python

import ROOT
import array

def readTree(filename):
    fIn = ROOT.TFile(filename, "READ")

    tree = fIn.Get("tree")

    #initialize a histogram
    histnFP = ROOT.TH1F("histnFP", "histnFP", 100, 0, 200)
    histpx = ROOT.TH1F("histpx", "histpx", 100, -2.5, 2.5)
    histpy = ROOT.TH1F("histpy", "histpy", 100, -2.5, 2.5)
    histpz = ROOT.TH1F("histpz", "histpz", 100, -3.5, 3.5)
    histenergy = ROOT.TH1F("histenergy", "histenergy", 100, 0, 5)
    histcharge = ROOT.TH1F("histcharge", "histcharge", 5, -2.5, 2.5)
    histmass = ROOT.TH1F("histmass", "histmass", 20, 0, 1)

    hist1mass = ROOT.TH1F("hist1mass", "hist1mass", 20, 0, 1)
    hist0mass = ROOT.TH1F("hist0mass", "hist0mass", 20, 0, 1)
    histneg1mass = ROOT.TH1F("histneg1mass", "histneg1mass", 20, 0, 1)

#this part!
    for i, value in enumerate(tree):
        #print("{0}: {1}".format(i, value.nFinalParticles))
        histnFP.Fill(value.nFinalParticles);
        for momentumX in value.px:
            #print("{0}".format(momentumX))
            histpx.Fill(momentumX)
        for i in value.py:
            histpy.Fill(i)
        for i in value.pz:
            histpz.Fill(i)
        for i in value.energy:
            histenergy.Fill(i)
        for i in value.charge:
            histcharge.Fill(i)

        for index, m in enumerate(value.mass):
            histmass.Fill(m)
            if value.charge[index] == 1:
                hist1mass.Fill(m)
            if value.charge[index] == 0:
                hist0mass.Fill(m)
            if value.charge[index] == -1:
                histneg1mass.Fill(m)

#initialize a canvas
    canvasnFP = ROOT.TCanvas("canvasnFP", "canvasnFP")
    canvaspx = ROOT.TCanvas("canvaspx", "canvaspx")
    canvaspy = ROOT.TCanvas("canvaspy", "canvaspy")
    canvaspz = ROOT.TCanvas("canvaspz", "canvaspz")
    canvasenergy = ROOT.TCanvas("canvasenergy", "canvasenergy")
    canvascharge = ROOT.TCanvas("canvascharge", "canvascharge")
    canvasmass = ROOT.TCanvas("canvasmass", "canvasmass")

    canvas1mass = ROOT.TCanvas("canvas1mass", "canvas1mass")
    canvas0mass = ROOT.TCanvas("canvas0mass", "canvas0mass")
    canvasneg1mass = ROOT.TCanvas("canvasneg1mass", "canvasneg1mass")

    canvasnFP.cd()
    histnFP.Draw()
    canvasnFP.SaveAs("nFPpy.pdf")

    canvaspx.cd()
    histpx.Draw()
    canvaspx.SaveAs("pxpy.pdf")

    canvaspy.cd()
    histpy.Draw()
    canvaspy.SaveAs("pypy.pdf")

    canvaspz.cd()
    histpz.Draw()
    canvaspz.SaveAs("pzpy.pdf")
    
    canvasenergy.cd()
    histenergy.Draw()
    canvasenergy.SaveAs("energypy.pdf")

    canvascharge.cd()
    histcharge.Draw()
    canvascharge.SaveAs("chargepy.pdf")

    canvasmass.cd()
    histmass.Draw()
    canvasmass.SaveAs("masspy.pdf")

    canvas1mass.cd()
    hist1mass.Draw()
    canvas1mass.SaveAs("mass1py.pdf")

    canvas0mass.cd()
    hist0mass.Draw()
    canvas0mass.SaveAs("mass0py.pdf")

    canvasneg1mass.cd()
    histneg1mass.Draw()
    canvasneg1mass.SaveAs("massneg1py.pdf")

#quasi-main
if __name__ == "__main__":
    filename = "ppfile.root"

    readTree(filename = filename)

