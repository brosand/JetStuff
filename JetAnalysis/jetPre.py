#input: a tree with all the particle data, a tree with all the jet data
#output: a tree where for each event, one branch for event number, one branch for number of jets, one branch is a vector of vectors containing the indices of each particle within a jet. This way with these indices we can go back to the tree and get information about these jets

import ROOT
import array

def readTree(filename1, filename2):
    fIn = ROOT.TFile(filename1, "READ")
    tree = fIn.Get("tree")

    #read in the other tree
    fIn = ROOT.TFile(filename2, "READ")
    jetTree = fIn.Get("jetTree")

    return tree, jetTree #will this work? if not put everything in this function

def preprocess(tree, jetTree):

    histcentre = ROOT.TH2F("histcentre", "histcentre", 100, 0, 250, 100, 0, 250) #bin bound bound bin bound bound
    histrotate = ROOT.TH2F("histrotate", "histrotate", 100, 0, 250, 100, 0, 250) #bin bound bound bin bound bound
    canvascentre = ROOT.TCanvas("canvascentre", "canvascentre")
    canvasrotate = ROOT.TCanvas("canvasrotate", "canvasrotate")

    for i, eventN in enumerate(jetTree):

        for j in range(nJets):

            maxm = pIndex[j][0]
            submax = pIndex[j][0] 

            for k, index in enumerate(pIndex[j]):
		#index will give the particle index, eg [7, 21, 32], k gives 0, 1, 2

                tree.eventN.energy[pIndex[j][k]]

                #finding the particles with the highest and second highest energy in the jet
                if tree.eventN.energy[pIndex[j][k]] > maxm:
                    maxm = pIndex[j][k]
                else if tree.eventN.energy[pIndex[j][k]] > submax:
                    submax = pIndex[j][k]

            star = arctan((tree.eventN.eta[maxm]-tree.eventN.eta[submax])/(tree.eventN.phi[maxm]-tree.eventN.phi[submax]))

            #define the jet axis -- ask Ben how the px py pz of the jet are defined
            phijet = math.acos(jetTree.eventN.px[j]/(math.sqrt(math.pow(jetTree.eventN.px[j], 2)+math.pow(jetTree.eventN.py[j], 2))))
            etajet = jetTree.eventN.pz[j]/(math.sqrt(math.pow(jetTree.eventN.px[j], 2) + math.pow(jetTree.eventN.px[j], 2) + math.pow(jetTree.eventN.px[j])))

            for k, index in enumerate(pIndex[j]):
                ptot = math.sqrt(math.pow(tree.eventN.px[index], 2) + math.pow(tree.eventN.px[index], 2) + math.pow(tree.eventN.px[index]))
                phi = math.acos(tree.eventN.px[index]/(math.sqrt(math.pow(tree.eventN.px[index], 2)+math.pow(tree.eventN.py[index], 2))))
                eta = tree.eventN.pz[index]/ptot

                #centre the jet axis
                phi = phi-phijet
                eta = eta-etajet

                #fill histogram for centre

                histcentre.Fill(phi, eta)

                #rotate
                           #check which arctan
                alpha = math.atan(eta/phi) #fill in numbers
                r = math.sqrt(math.pow(phi, 2) + math.pow(eta, 2))
                phi = r * math.cos(alpha-star)
                eta = r * math.sin(alpha-star)
                
                #fill histogram for rotate
                histrotate.Fill(phi, eta)       

'''copied part
        for momentumX in event.px:
            #print("{0}".format(momentumX))
            histpx.Fill(momentumX)
        for i in event.py:
            histpy.Fill(i)
        for i in event.pz:
            histpz.Fill(i)
        for i in event.energy:
            histenergy.Fill(i)
        for i in event.charge:
            histcharge.Fill(i)

        for index, m in enumerate(event.mass):
            histmass.Fill(m)
            if event.charge[index] == 1:
                hist1mass.Fill(m)
            if event.charge[index] == 0:
                hist0mass.Fill(m)
            if event.charge[index] == -1:
                histneg1mass.Fill(m)
#end of copied part'''

    canvascentre.cd()
    histcentre.Draw()
    canvascentre.SaveAs("centre.pdf")

    canvasrotate.cd()
    histrotate.Draw()
    canvasrotate.SaveAs("rotate.pdf")

#quasi-main
if __name__ == "__main__":
    filename1 = "pbfile.root"
    filename2 = "jetFile.root"

    readTree(filename1 = filename1, filename2 = filename2)
    preprocess(tree, jetTree)

