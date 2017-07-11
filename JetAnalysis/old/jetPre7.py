#input: a tree with all the particle data, a tree with all the jet data
#output: a tree where for each event, one branch for event number, one branch for number of jets, one branch is a vector of vectors containing the indices of each particle within a jet. This way with these indices we can go back to the tree and get information about these jets
from itertools import izip
import ROOT
import array
import numpy
import math

DIMENSION_JET_IMAGE = 3
COLLISION_TYPE = "pp"

def printOutput(output, j, iEvent, histogram):
    output.write(COLLISION_TYPE)
    for q in range(DIMENSION_JET_IMAGE):
        for r in range(DIMENSION_JET_IMAGE):
            output.write(" %f  " % histogram.GetBinContent(q + 1, r + 1))
    output.write(" %d %d \n" % (j, iEvent))
    print(histogram[0])
    print('histogram at 1,1')
    print(histogram.GetBinContent(1,1))
    print('histogram at 2,2')
    print(histogram.GetBinContent(2,2))



def getPhi(pEvent, index):
    if(pEvent.py[index]<0):
        phi = (-1)*math.acos(pEvent.px[index]/(math.sqrt(math.pow(pEvent.px[index], 2)+math.pow(pEvent.py[index], 2))))
    else:
        phi = math.acos(pEvent.px[index]/(math.sqrt(math.pow(pEvent.px[index], 2)+math.pow(pEvent.py[index], 2))))
    
    return phi

def getEta(pEvent, index):
    pTot = math.sqrt(math.pow(pEvent.px[index], 2) + math.pow(pEvent.py[index], 2) + math.pow(pEvent.pz[index], 2))
    eta = math.atanh(pEvent.pz[index]/pTot)
    
    return eta

def fCentre(jEvent, j, phi, eta):


    phijet = jEvent.phi[j]
    etajet = jEvent.eta[j]
#translation 1: centering 
    phi = phi-phijet
    eta = eta-etajet
    # phi_maxm = phi_maxm-phijet
    # eta_maxm = eta_maxm-etajet

    # phi_submax = phi_submax-phijet
    # eta_submax = eta_submax-etajet
    return phi, eta

def findMaxSubmax(jEvent, pEvent, j):
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

    return phi_maxm, eta_maxm, phi_submax, eta_maxm

def fRotate(jEvent, j, phi, eta, phi_maxm, eta_maxm, phi_submax, eta_submax):
    if(len(jEvent.pIndex[j])>1):

        star = math.atan2((eta_maxm-eta_submax), (phi_maxm-phi_submax))

        alpha = math.atan2(eta,phi) #fill in numbers
        r = math.sqrt(math.pow(phi, 2) + math.pow(eta, 2))
        phi = r * math.cos(alpha-star)
        eta = r * math.sin(alpha-star)

    return phi, eta

def fTranslate(phi, eta, phi_maxm, eta_maxm):
    phi = phi - phi_maxm
    eta = eta - eta_maxm

    return phi, eta

def fReflect_Fill_Print(output, iEvent, jEvent, j, phiTempV, etaTempV, energyTempV, sumEtaPos, sumEtaNeg):
    if(len(jEvent.pIndex[j])>1):
        for i, a in enumerate(etaTempV):
            if(sumEtaPos < sumEtaNeg):
                a = -1*a
        #fill the histogram for reflection
            histReflect.Fill(phiTempV[i], a, energyTempV[i])
        #fill a temporary histogram with data from one jet
            histJetTemp.Fill(phiTempV[i], a, energyTempV[i])
        printOutput(output, j, iEvent, histJetTemp)
        etaTempV = []
        phiTempV = []
        energyTempV = []
        histJetTemp.Reset()

    return etaTempV
    



def readTree(filename1, filename2):

    fIn = ROOT.TFile(filename1, "READ")
    tree = fIn.Get("tree")
    tree.Print()
    #read in the other tree
    fIn2 = ROOT.TFile(filename2, "READ")
    jetTree = fIn2.Get("jetTree")
    jetTree.Print()

    histBefore = ROOT.TH2F("histBefore", "histBefore", DIMENSION_JET_IMAGE, -4, 4, DIMENSION_JET_IMAGE, -4, 4) #bin bound bound bin bound bound
    histBefore.GetXaxis().SetTitle("phi");
    histBefore.GetYaxis().SetTitle("eta");
    histBefore.GetZaxis().SetTitle("counts weighted by energy");

    histCentre = ROOT.TH2F("histCentre", "histCentre", DIMENSION_JET_IMAGE, -1, 1, DIMENSION_JET_IMAGE, -1, 1) #bin bound bound bin bound bound
    histCentre.GetXaxis().SetTitle("phi");
    histCentre.GetYaxis().SetTitle("eta");
    histCentre.GetZaxis().SetTitle("counts weighted by energy");

    histRotate = ROOT.TH2F("histRotate", "histRotate", DIMENSION_JET_IMAGE, -1, 1, DIMENSION_JET_IMAGE, -1, 1) #bin bound bound bin bound bound
    histRotate.GetXaxis().SetTitle("phi");
    histRotate.GetYaxis().SetTitle("eta");
    histRotate.GetZaxis().SetTitle("counts weighted by energy");

    histTranslate = ROOT.TH2F("histTranslate", "histTranslate", DIMENSION_JET_IMAGE, -1, 1, DIMENSION_JET_IMAGE, -1, 1) #bin bound bound bin bound bound
    histTranslate.GetXaxis().SetTitle("phi");
    histTranslate.GetYaxis().SetTitle("eta");
    histTranslate.GetZaxis().SetTitle("counts weighted by energy");

    histReflect = ROOT.TH2F("histReflect", "histReflect", DIMENSION_JET_IMAGE, -1, 1, DIMENSION_JET_IMAGE, -1, 1) #bin bound bound bin bound bound
    histReflect.GetXaxis().SetTitle("phi");
    histReflect.GetYaxis().SetTitle("eta");
    histReflect.GetZaxis().SetTitle("counts weighted by energy");

    histJetTemp = ROOT.TH2F("histJetTemp", "histJetTemp", DIMENSION_JET_IMAGE, -1, 1, DIMENSION_JET_IMAGE, -1, 1) # numBins bound bound bin bound bound
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
    open('outputC.txt', 'w').close()
    iEvent = 0;
    outputC = open("outputC.txt" , "w" )

    open('outputR.txt', 'w').close()
    iEvent = 0;
    outputR = open("outputR.txt" , "w" )

    open('outputT.txt', 'w').close()
    iEvent = 0;
    outputT = open("outputT.txt" , "w" )

    open('outputF.txt', 'w').close()
    iEvent = 0;
    outputF = open("outputF.txt" , "w" )

#LOOP: through each event in tree
    for pEvent, jEvent in  izip(tree, jetTree): #zip

        if (iEvent == 1):
            break
        print("Event %d:" % iEvent)
    #for event in jetTree:
        print("jEvent.nJets is %d" %jEvent.nJets)
        print("pEvent.nParticles is %d" %pEvent.nFinalParticles)
#LOOP: through each jet in event    
        for j in range(1): #j tells you which jet you are in
             
            print("\tJet number %d" %j)
            print("\tjEvent.pIndex[j][0] = %d" % jEvent.pIndex[j][0])
            
            #max placeholder for finding highest-energy particle in a jet
            #loop through and find max energy
            # maxm = jEvent.pIndex[j][0]
#LOOP: through each particle in jet
       #      for k, index in enumerate(jEvent.pIndex[j]):
       # #index will give the particle index, eg [7, 21, 32], k gives 0, 1, 2
       #          print("\t\t\tenergy[%d] = %f" % (jEvent.pIndex[j][k], pEvent.energy[jEvent.pIndex[j][k]]))
       #          #events[0].energy[event[1].pIndex[j][k]] #how to tap into event number on other tree
       #          #tree.event.energy[event.pIndex[j][k]] #how to tap into event number on other tree
                 
       #          #finding the particle in the jet with the highest energy
       #          if pEvent.energy[jEvent.pIndex[j][k]] > pEvent.energy[maxm]:
       #              maxm = jEvent.pIndex[j][k]
       #      print("\t\tmax: %d" % maxm)
       #      phi_maxm = math.acos(pEvent.px[maxm]/(math.sqrt(math.pow(pEvent.px[maxm], 2)+math.pow(pEvent.py[maxm], 2))))
       #      eta_maxm = math.atanh(pEvent.pz[maxm]/(math.sqrt(math.pow(pEvent.px[maxm], 2) + math.pow(pEvent.py[maxm], 2) + math.pow(pEvent.pz[maxm], 2))))
       #      submax = 0
       #      # phi_submax = 0
       #      # eta_submax = 0
       #      if(len(jEvent.pIndex[j])>1):
       #          if (maxm == jEvent.pIndex[j][0]):
       #             submax = jEvent.pIndex[j][1]
       #          else:
       #             submax = jEvent.pIndex[j][0]
       #          for k, index in enumerate(jEvent.pIndex[j]): #finding the particle in the jet with the second highest energy

       #              if ((pEvent.energy[submax] < pEvent.energy[jEvent.pIndex[j][k]]) and (pEvent.energy[jEvent.pIndex[j][k]] < pEvent.energy[maxm])):
       #                  submax = jEvent.pIndex[j][k]
       #          print("\t\tsubmax: %d" % submax)
                
       #          phi_submax = math.acos(pEvent.px[submax]/(math.sqrt(math.pow(pEvent.px[submax], 2)+math.pow(pEvent.py[submax], 2))))
       #          eta_submax = math.atanh(pEvent.pz[submax]/(math.sqrt(math.pow(pEvent.px[submax], 2) + math.pow(pEvent.py[submax], 2) + math.pow(pEvent.pz[submax], 2))))
    
    
            phiTempV = []
            etaTempV = []
            energyTempV = []
            sumEtaPos = 0
            sumEtaNeg = 0

            phi_maxm, eta_maxm, phi_submax, eta_submax = findMaxSubmax(jEvent, pEvent, j)
            phi_maxm, eta_maxm = fCentre(jEvent, j, phi_maxm, eta_maxm)
            phi_submax, eta_submax = fCentre(jEvent, j, phi_submax, eta_submax)
            phi_maxm, eta_maxm = fRotate(jEvent, j, phi_maxm, eta_maxm, phi_maxm, eta_maxm, phi_submax, eta_submax)

            for index in (jEvent.pIndex[j]):
                phi, eta = getPhi(pEvent, index), getEta(pEvent, index)
                histBefore.Fill(phi, eta, pEvent.energy[index])
                
                phi, eta = fCentre(jEvent, j, phi, eta)
                histCentre.Fill(phi, eta, pEvent.energy[index])
                #centre the max and submax
                
                phi, eta = fRotate(jEvent, j, phi, eta, phi_maxm, eta_maxm, phi_submax, eta_submax)
                histRotate.Fill(phi, eta, pEvent.energy[index])

                phi, eta = fTranslate(phi, eta, phi_maxm, eta_maxm)
                histTranslate.Fill(phi , eta, pEvent.energy[index])

                if(eta > 0):
                    sumEtaPos += pEvent.energy[index]
                elif(eta < 0):
                    sumEtaNeg += pEvent.energy[index]
                
                etaTempV.append(eta)
                phiTempV.append(phi)
                energyTempV.append(pEvent.energy[index])
            etaTempv = fReflect(output, iEvent, jEvent, j, phiTempV, etaTempV, energyTempV, sumEtaPos, sumEtaNeg)
                
               



        #         before anything

        # center the jet axis
        #         phijet = jEvent.phi[j]
        #         etajet = jEvent.eta[j]
        #   #translation 1: centering 
        #         phi = phi-phijet
        #         eta = eta-etajet

        #         phi_maxm = phi_maxm-phijet
        #         eta_maxm = eta_maxm-etajet

        #         phi_submax = phi_submax-phijet
        #         eta_submax = eta_submax-etajet

                
        #         fill histogram for centre
        #     ########
        #     rotate
        #         if(len(jEvent.pIndex[j])>1):

        #             star = math.atan2((eta_maxm-eta_submax), (phi_maxm-phi_submax))

        #                    #check which arctan
        #             alpha = math.atan2(eta,phi) #fill in numbers
        #             r = math.sqrt(math.pow(phi, 2) + math.pow(eta, 2))
        #             phi = r * math.cos(alpha-star)
        #             eta = r * math.sin(alpha-star)

        #             #Translation pt 2


        #         # fill histogram for rotate
        #             histRotate.Fill(phi, eta, pEvent.energy[index])

        #             alpha_maxR = math.atan2(eta_maxm,phi_maxm) #fill in numbers
        #             r_maxR = math.sqrt(math.pow(phi_maxm, 2) + math.pow(eta_maxm, 2))
        #             phi_maxR = r_maxR * math.cos(alpha_maxR-star)
        #             eta_maxR = r_maxR * math.sin(alpha_maxR-star) 

        #             alpha_submax = math.atan2(eta_submax,phi_submax) #fill in numbers
        #             r_submax = math.sqrt(math.pow(phi_submax, 2) + math.pow(eta_submax, 2))
        #             phi_submax = r_submax * math.cos(alpha_submax-star)
        #             eta_submax = r_submax * math.sin(alpha_submax-star)                   
        #             next step of translation
        #             print ('phi: %f phi-maxm: %f ' % (phi, phi_maxm))
        #             print ('eta: %f eta-maxm: %f ' % (eta, eta_maxm))

                     # phi = phi - phi_maxR
                     # eta = eta - eta_maxR

                   


                   
                    #reflect


                    #do the reflection
                    #put greater energy in positive eta(quadrants 1&2)
                #if(jEvent.pIndex[i]  

            #write the temporary histogram to a text file
                printOutput(outputC, j, iEvent, histCentre)
                printOutput(outputR, j, iEvent, histRotate)
                printOutput(outputT, j, iEvent, histTranslate)
                printOutput(outputF, j, iEvent, histJetTemp)
            
                # output.write(COLLISION_TYPE)
                # for q in range(DIMENSION_JET_IMAGE):
                #     for r in range(DIMENSION_JET_IMAGE):
                #         output.write(" %d  " % histJetTemp.GetBinContent(q, r))
                # output.write(" %d %d \n" % (j, iEvent))
                # print(histJetTemp[0])
                # print(histJetTemp.GetBinContent(1,1))
                # print(histJetTemp.GetBinContent(2,2))




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


