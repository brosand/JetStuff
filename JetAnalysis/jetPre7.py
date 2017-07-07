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

    histbefore = ROOT.TH2F("histbefore", "histbefore", 20, -2, 2, 20, -2, 2) #bin bound bound bin bound bound
    histbefore.GetXaxis().SetTitle("phi");
    histbefore.GetYaxis().SetTitle("eta");
    histbefore.GetZaxis().SetTitle("idk");
    histcentre = ROOT.TH2F("histcentre", "histcentre", 20, -2, 2, 20, -2, 2) #bin bound bound bin bound bound
    histcentre.GetXaxis().SetTitle("phi");
    histcentre.GetYaxis().SetTitle("eta");
    histcentre.GetZaxis().SetTitle("idk");
    histrotate = ROOT.TH2F("histrotate", "histrotate", 20, -2, 2, 20, -2, 2) #bin bound bound bin bound bound
    histrotate.GetXaxis().SetTitle("phi");
    histrotate.GetYaxis().SetTitle("eta");
    histrotate.GetZaxis().SetTitle("idk");
    histTranslate = ROOT.TH2F("histTranslate", "histTranslate", 50, -1, 1, 50, -1, 1) #bin bound bound bin bound bound
    histTranslate.GetXaxis().SetTitle("phi");
    histTranslate.GetYaxis().SetTitle("eta");
    histTranslate.GetZaxis().SetTitle("idk");
    canvasbefore = ROOT.TCanvas("canvasbefore", "canvasbefore")
    canvascentre = ROOT.TCanvas("canvascentre", "canvascentre")
    canvasrotate = ROOT.TCanvas("canvasrotate", "canvasrotate")
    canvasTranslate = ROOT.TCanvas("canvasTranslate", "canvasTranslate")

    '''

    for i, (a, b) in enumerate(tuple_list):
        new_b = some_process(b)
        tuple_list[i] = (a, new_b)

    '''
    iEvent = 0;
    for pEvent, jEvent in  izip(tree, jetTree): #zip
        print("Event %d:" % iEvent)
        iEvent+=1
    #for event in jetTree:
        print("jEvent.nJets is %d" %jEvent.nJets)
        print("pEvent.nParticles is %d" %pEvent.nFinalParticles)
        
        for j in range(jEvent.nJets): #j tells you which jet you are in
            print("\tJet number %d" %j)
            print("\tjEvent.pIndex[j][0] = %d" % jEvent.pIndex[j][0])
            
            #max placeholder for finding highest-energy particle in a jet
            #loop through and find max energy
            maxm = jEvent.pIndex[j][0]
            for k, index in enumerate(jEvent.pIndex[j]):
       #index will give the particle index, eg [7, 21, 32], k gives 0, 1, 2
                print("\t\t\tenergy[%d] = %f" % (jEvent.pIndex[j][k], pEvent.energy[jEvent.pIndex[j][k]]))
                #events[0].energy[event[1].pIndex[j][k]] #how to tap into event number on other tree
                #tree.event.energy[event.pIndex[j][k]] #how to tap into event number on other tree
                 
                #finding the particle in the jet with the highest energy
                if pEvent.energy[jEvent.pIndex[j][k]] > pEvent.energy[maxm]:
                    maxm = jEvent.pIndex[j][k]
            print("\t\tmax: %d" % maxm)
            phi_maxm = math.acos(pEvent.px[maxm]/(math.sqrt(math.pow(pEvent.px[maxm], 2)+math.pow(pEvent.py[maxm], 2))))
            eta_maxm = math.atanh(pEvent.pz[maxm]/(math.sqrt(math.pow(pEvent.px[maxm], 2) + math.pow(pEvent.py[maxm], 2) + math.pow(pEvent.pz[maxm], 2))))
            submax = 0
            # phi_submax = 0
            # eta_submax = 0
            if(len(jEvent.pIndex[j])>1):
                if (maxm == jEvent.pIndex[j][0]):
                   submax = jEvent.pIndex[j][1]
                else:
                   submax = jEvent.pIndex[j][0]
                for k, index in enumerate(jEvent.pIndex[j]): #finding the particle in the jet with the second highest energy

                    if ((pEvent.energy[submax] < pEvent.energy[jEvent.pIndex[j][k]]) and (pEvent.energy[jEvent.pIndex[j][k]] < pEvent.energy[maxm])):
                        submax = jEvent.pIndex[j][k]
                print("\t\tsubmax: %d" % submax)
                
                phi_submax = math.acos(pEvent.px[submax]/(math.sqrt(math.pow(pEvent.px[submax], 2)+math.pow(pEvent.py[submax], 2))))
                eta_submax = math.atanh(pEvent.pz[submax]/(math.sqrt(math.pow(pEvent.px[submax], 2) + math.pow(pEvent.py[submax], 2) + math.pow(pEvent.pz[submax], 2))))

            for index in (jEvent.pIndex[j]):
                pTot = math.sqrt(math.pow(pEvent.px[index], 2) + math.pow(pEvent.py[index], 2) + math.pow(pEvent.pz[index], 2))
                if(pEvent.py[index]<0):
                    phi = (-1)*math.acos(pEvent.px[index]/(math.sqrt(math.pow(pEvent.px[index], 2)+math.pow(pEvent.py[index], 2))))
                else:
                    phi = math.acos(pEvent.px[index]/(math.sqrt(math.pow(pEvent.px[index], 2)+math.pow(pEvent.py[index], 2))))
                eta = math.atanh(pEvent.pz[index]/pTot)

                #before anything
                histbefore.Fill(phi, eta)

        #center the jet axis
                phijet = jEvent.phi[j]
                etajet = jEvent.eta[j]
          #translation 1: centering 
                phi = phi-phijet
                eta = eta-etajet

                phi_maxm = phi_maxm-phijet
                eta_maxm = eta_maxm-etajet

                phi_submax = phi_submax-phijet
                eta_submax = eta_submax-etajet


                #fill histogram for centre
                histcentre.Fill(phi, eta)
            #########
            #rotate
                if(len(jEvent.pIndex[j])>1):

                    star = math.atan2((phi_maxm-phi_submax),(eta_maxm-eta_submax))

                           #check which arctan
                    alpha = math.atan2(eta,phi) #fill in numbers
                    r = math.sqrt(math.pow(phi, 2) + math.pow(eta, 2))
                    phi = r * math.cos(alpha-star)
                    eta = r * math.sin(alpha-star)

                    alpha_maxm = math.atan2(eta_maxm,phi_maxm) #fill in numbers
                    r_maxm = math.sqrt(math.pow(phi_maxm, 2) + math.pow(eta_maxm, 2))
                    phi_maxm = r_maxm * math.cos(alpha_maxm-star)
                    eta_maxm = r_maxm * math.sin(alpha_maxm-star) 

                    alpha_submax = math.atan2(eta_submax,phi_submax) #fill in numbers
                    r_submax = math.sqrt(math.pow(phi_submax, 2) + math.pow(eta_submax, 2))
                    phi_submax = r_submax * math.cos(alpha_submax-star)
                    eta_submax = r_submax * math.sin(alpha_submax-star)                   
                    #Translation pt 2


                # fill histogram for rotate
                    histrotate.Fill(phi, eta)
                    #next step of translation
                    phi = phi - phi_maxm
                    eta = eta - eta_maxm


                    histTranslate.Fill(phi,eta)
                   
                    #reflect
                    sumetapos = 0
                    sumetaneg = 0
                    if(eta >=0):
                        sumetapos += pEvent.energy[index]
                    else:
                        sumetaneg += pEvent.energy[index]

                    



    #see others for examples of iterating through
    canvasbefore.cd()
    histbefore.Draw("lego")
    canvasbefore.SaveAs("before.pdf")

    canvascentre.cd()
    histcentre.Draw("lego")
    #https://root.cern.ch/root/html534/guides/users-guide/Histograms.html
    canvascentre.SaveAs("centre.pdf")

    canvasrotate.cd()
    histrotate.Draw("lego")
    canvasrotate.SaveAs("rotate.pdf")

    canvasTranslate.cd()
    histTranslate.Draw("lego")
    canvasTranslate.SaveAs("translate.pdf")

    

if __name__ == "__main__":
    filename1 = "ppfile.root"
    filename2 = "jetFile.root"

    readTree(filename1 = filename1, filename2 = filename2)
    

