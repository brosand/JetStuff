#input: a tree with all the particle data, a tree with all the jet data
#output: a tree where for each event, one branch for event number, one branch for number of jets, one branch is a vector of vectors containing the indices of each particle within a jet. This way with these indices we can go back to the tree and get information about these jets
from itertools import izip
import ROOT
import array
import numpy
import math
def readTree(filename1, filename2):

    DIMENSION_JET_IMAGE = 3
    COLLISION_TYPE = "pp"

    fIn = ROOT.TFile(filename1, "READ")
    tree = fIn.Get("tree")
    tree.Print()
    #read in the other tree
    fIn2 = ROOT.TFile(filename2, "READ")
    jetTree = fIn2.Get("jetTree")
    jetTree.Print()

    histBefore = ROOT.TH2F("histBefore", "histBefore", 20, -2, 2, 20, -2, 2) #bin bound bound bin bound bound
    histBefore.GetXaxis().SetTitle("phi");
    histBefore.GetYaxis().SetTitle("eta");
    histBefore.GetZaxis().SetTitle("counts weighted by energy");

    histCentre = ROOT.TH2F("histCentre", "histCentre", 20, -2, 2, 20, -2, 2) #bin bound bound bin bound bound
    histCentre.GetXaxis().SetTitle("phi");
    histCentre.GetYaxis().SetTitle("eta");
    histCentre.GetZaxis().SetTitle("counts weighted by energy");

    histRotate = ROOT.TH2F("histRotate", "histRotate", 20, -2, 2, 20, -2, 2) #bin bound bound bin bound bound
    histRotate.GetXaxis().SetTitle("phi");
    histRotate.GetYaxis().SetTitle("eta");
    histRotate.GetZaxis().SetTitle("counts weighted by energy");

    histTranslate = ROOT.TH2F("histTranslate", "histTranslate", 20, -1, 1, 20, -1, 1) #bin bound bound bin bound bound
    histTranslate.GetXaxis().SetTitle("phi");
    histTranslate.GetYaxis().SetTitle("eta");
    histTranslate.GetZaxis().SetTitle("counts weighted by energy");

    histReflect = ROOT.TH2F("histReflect", "histReflect", 20, -1, 1, 20, -1, 1) #bin bound bound bin bound bound
    histReflect.GetXaxis().SetTitle("phi");
    histReflect.GetYaxis().SetTitle("eta");
    histReflect.GetZaxis().SetTitle("counts weighted by energy");

    histJetTemp = ROOT.TH2F("histJetTemp", "histJetTemp", DIMENSION_JET_IMAGE, -5, 5, DIMENSION_JET_IMAGE, -5, 5) # numBins bound bound bin bound bound
    histJetTemp.GetXaxis().SetTitle("phi");
    histJetTemp.GetYaxis().SetTitle("eta");
    histJetTemp.GetZaxis().SetTitle("counts weighted by energy");

    canvasBefore = ROOT.TCanvas("canvasBefore", "canvasBefore")
    canvasCentre = ROOT.TCanvas("canvasCentre", "canvasCentre")
    canvasRotate = ROOT.TCanvas("canvasRotate", "canvasRotate")
    canvasTranslate = ROOT.TCanvas("canvasTranslate", "canvasTranslate")
    canvasReflect = ROOT.TCanvas("canvasReflect", "canvasReflect")

    '''

    for i, (a, b) in enumerate(tuple_list):
        new_b = some_process(b)
        tuple_list[i] = (a, new_b)

    '''
    open('output.txt', 'w').close()
    iEvent = 0;
    output = open("output.txt" , "w" )

#LOOP: through each event in tree
    for pEvent, jEvent in  izip(tree, jetTree): #zip
        print("Event %d:" % iEvent)
    #for event in jetTree:
        print("jEvent.nJets is %d" %jEvent.nJets)
        print("pEvent.nParticles is %d" %pEvent.nFinalParticles)
#LOOP: through each jet in event    
        for j in range(jEvent.nJets): #j tells you which jet you are in
             
            print("\tJet number %d" %j)
            print("\tjEvent.pIndex[j][0] = %d" % jEvent.pIndex[j][0])
            
            #max placeholder for finding highest-energy particle in a jet
            #loop through and find max energy
            maxm = jEvent.pIndex[j][0]
            phiTempV = []
            etaTempV = []
            energyTempV = []
            sumEtaPos = 0
            sumEtaNeg = 0
#LOOP: through each particle in jet
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
                histBefore.Fill(phi, eta, pEvent.energy[index])

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
                histCentre.Fill(phi, eta, pEvent.energy[index])
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
                    histRotate.Fill(phi, eta)
                    #next step of translation
                    phi = phi - phi_maxm
                    eta = eta - eta_maxm


                    histTranslate.Fill(phi,eta, pEvent.energy[index])
                   
                    #reflect
                    etaTempV.append(eta)
                    phiTempV.append(phi)
                    energyTempV.append(pEvent.energy[index])

                    if(eta > 0):
                        sumEtaPos += pEvent.energy[index]
                    elif(eta < 0):
                        sumEtaNeg += pEvent.energy[index]

                    #do the reflection
                    #put greater energy in positive eta(quadrants 1&2)
            for i, a in enumerate(etaTempV):
                if(sumEtaPos < sumEtaNeg):
                    a = -1*a
            #fill the histogram for reflection
                histReflect.Fill(phiTempV[i], a, energyTempV[i])
            #fill a temporary histogram with data from one jet
                histJetTemp.Fill(phiTempV[i],etaTempV[i], energyTempV[i])
            # if(jEvent.pIndex[i]  

            #write the temporary histogram to a text file
            
            output.write(COLLISION_TYPE)
            for q in range(DIMENSION_JET_IMAGE):
                for n in range(DIMENSION_JET_IMAGE):
                    output.write(" %d " % histJetTemp.GetBinContent(q, n))
            output.write(" %d %d \n" % (j, iEvent))


            etaTempV = []
            phiTempV = []
            energyTempV = []
            histJetTemp.Reset()

        iEvent+=1


    #see others for examples of iterating through
    canvasBefore.cd()
    histBefore.Draw("lego")
    canvasBefore.SaveAs("before.pdf")

    canvasCentre.cd()
    histCentre.Draw("lego")
    #https://root.cern.ch/root/html534/guides/users-guide/Histograms.html
    canvasCentre.SaveAs("centre.pdf")

    canvasRotate.cd()
    histRotate.Draw("lego")
    canvasRotate.SaveAs("rotate.pdf")

    canvasTranslate.cd()
    histTranslate.Draw("lego")
    canvasTranslate.SaveAs("translate.pdf")

    canvasReflect.cd()
    histReflect.Draw("lego")
    canvasReflect.SaveAs("reflect.pdf")
    

if __name__ == "__main__":
    filename1 = "ppfile.root"
    filename2 = "jetFile.root"

    readTree(filename1 = filename1, filename2 = filename2)
    

