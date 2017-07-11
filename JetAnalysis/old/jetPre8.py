#most updated version, now trying Helen's way of iterating through events

#input: a tree with all the particle data, a tree with all the jet data
#output: a tree where for each event, one branch for event number, one branch for number of jets, one branch is a vector of vectors containing the indices of each particle within a jet. This way with these indices we can go back to the tree and get information about these jets
from itertools import izip
import ROOT
import array
import numpy
import math
def readTree(filename1, filename2):
    fIn = ROOT.TFile(filename1, "READ")
    tree = fIn.Get("tree")
    tree.Print()
    #read in the other tree
    fIn2 = ROOT.TFile(filename2, "READ")
    jetTree = fIn2.Get("jetTree")
    jetTree.Print()

    histcentre = ROOT.TH2F("histcentre", "histcentre", 100, -50, 50, 100, -50, 50) #bin bound bound bin bound bound
    histrotate = ROOT.TH2F("histrotate", "histrotate", 100, -50, 50, 100, -50, 50) #bin bound bound bin bound bound
    canvascentre = ROOT.TCanvas("canvascentre", "canvascentre")
    canvasrotate = ROOT.TCanvas("canvasrotate", "canvasrotate")

    iEvent = 0;
    njEvents = jetTree.GetEntries()
    npEvents = tree.GetEntries()
    if(njEvents != npEvents):
        print("Error. Trees do not match in length.")
        return
    for iEvent in range (njEvents):
        print("Event %d:" % iEvent)
        jEvent = jetTree.GetEntry(iEvent)
        pEvent = tree.GetEntry(iEvent)

        print("jEvent.nJets is %d" %jetTree.nJets)      
        
        for j in range(jetTree.nJets): #j tells you which jet you are in
            print("\tJet number %d" %j)
            print("\tjetTree.pIndex[j][0] = %d" % jetTree.pIndex[j][0])
            
            #max placeholder for finding highest-energy particle in a jet
            maxm = jetTree.pIndex[j][0]
            #loop through and find max energy
            for k, index in enumerate(jetTree.pIndex[j]):
       #index will give the particle index, eg [7, 21, 32], k gives 0, 1, 2
                print("\t\t\tenergy[%d] = %f" % (jetTree.pIndex[j][k], tree.energy[jetTree.pIndex[j][k]]))
                #events[0].energy[event[1].pIndex[j][k]] #how to tap into event number on other tree
                #tree.event.energy[event.pIndex[j][k]] #how to tap into event number on other tree
                 
                #finding the particle in the jet with the highest energy
                if tree.energy[jetTree.pIndex[j][k]] > tree.energy[maxm]:
                    maxm = jetTree.pIndex[j][k]

            print("\t\tmax: %d" % maxm)

            if(len(jetTree.pIndex[j])>1):
                if (maxm == jetTree.pIndex[j][0]):
                   submax = jetTree.pIndex[j][1]
                else:
                   submax = jetTree.pIndex[j][0]
                for k, index in enumerate(jetTree.pIndex[j]): #finding the particle in the jet with the second highest energy

                    if ((tree.energy[submax] < tree.energy[jetTree.pIndex[j][k]]) and (tree.energy[jetTree.pIndex[j][k]] < tree.energy[maxm])):
                        submax = jetTree.pIndex[j][k]
                print("\t\tsubmax: %d" % submax)
    '''
        for k, index in enumerate(jetTree.pIndex[j]):
            #centre the jet axis
            phi = phi-phijet #fix this
            eta = eta-etajet
        #fill histogram for centre
            histcentre.Fill(phi, eta)
            #############

        if(len(jetTree.pIndex[j])>1):

            star = numpy.arctan((jetTree.eta[maxm]-jetTree.eta[submax])/(jetTree.phi[maxm]-jetTree.phi[submax]))
    
        #     #define the jet axis
            phijet = jetTree.phi[j]
        # etajet = jetTree.eta[j]

        # for k, index in enumerate(jEvent.pIndex[j]):
        #     ptot = math.sqrt(math.pow(pEvent.px[index], 2) + math.pow(pEvent.px[index], 2) + math.pow(pEvent.px[index], 2))
        #     phi = math.acos(pEvent.px[index]/(math.sqrt(math.pow(pEvent.px[index], 2)+math.pow(pEvent.py[index], 2))))
        #     eta = pEvent.pz[index]/ptot

        #         #centre the jet axis
        #     phi = phi-phijet
        #     eta = eta-etajet

        #         #fill histogram for centre

        #     histcentre.Fill(phi, eta)

        #         #rotate
        #                    #check which arctan
        #     alpha = math.atan(eta/phi) #fill in numbers
        #     r = math.sqrt(math.pow(phi, 2) + math.pow(eta, 2))
        #     phi = r * math.cos(alpha-star)
        #     eta = r * math.sin(alpha-star)
                
                # fill histogram for rotate
            # histrotate.Fill(phi, eta)       
    #see others for examples of iterating through
        
    canvascentre.cd()
    histcentre.Draw("lego")
    #https://root.cern.ch/root/html534/guides/users-guide/Histograms.html
    canvascentre.SaveAs("centre.pdf")

    canvasrotate.cd()
    histrotate.Draw("lego")
    canvasrotate.SaveAs("rotate.pdf")
    '''

if __name__ == "__main__":
    filename1 = "ppfile.root"
    filename2 = "jetFile.root"

    readTree(filename1 = filename1, filename2 = filename2)
    

