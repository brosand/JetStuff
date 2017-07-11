#input: a tree with all the particle data, a tree with all the jet data
#output: a tree where for each event, one branch for event number, one branch for number of jets, one branch is a vector of vectors containing the indices of each particle within a jet. This way with these indices we can go back to the tree and get information about these jets
from itertools import izip
import ROOT
import array
import numpy
import math

<<<<<<< HEAD
COLLISION_TYPE = "pp"
HIST_BOUND = .6

def printOutput(output, j, iEvent, histogram, dimension):
    output.write(COLLISION_TYPE)
    for q in range(dimension):
        for r in range(dimension):
=======
DIMENSION_JET_IMAGE = 3
# COLLISION_TYPE = "pp"
HIST_BOUND = .6

def printOutput(output, j, iEvent, histogram, collisionType):
    output.write(collisionType)
    for q in range(DIMENSION_JET_IMAGE):
        for r in range(DIMENSION_JET_IMAGE):
>>>>>>> 4bd56d7edc09ecefaadffc3d7b1814d5225458cf
            output.write(" %f" % histogram.GetBinContent(q + 1, r + 1))
    output.write(" %d %d \n" % (j, iEvent))
    # print(histogram[0])
    # print('histogram at 1,1')
    # print(histogram.GetBinContent(1,1))
    # print('histogram at 2,2')
    # print(histogram.GetBinContent(2,2))



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


    # print('phi before centre: %f' % phi)
    phijet = jEvent.phi[j]
    etajet = jEvent.eta[j]
    # print('phijet: %f' % phijet)
#translation 1: centering 
    phi = phi-phijet
    eta = eta-etajet
    # print('phi after centre: %f' % phi)

    return phi, eta

def findMaxSubmax(jEvent, pEvent, j):
    maxm = jEvent.pIndex[j][0]

    for k, index in enumerate(jEvent.pIndex[j]):
#index will give the particle index, eg [7, 21, 32], k gives 0, 1, 2
        # print("\t\t\tenergy[%d] = %f" % (jEvent.pIndex[j][k], pEvent.energy[jEvent.pIndex[j][k]]))
        #events[0].energy[event[1].pIndex[j][k]] #how to tap into event number on other tree
        #tree.event.energy[event.pIndex[j][k]] #how to tap into event number on other tree
         
        #finding the particle in the jet with the highest energy
        if pEvent.energy[jEvent.pIndex[j][k]] > pEvent.energy[maxm]:
            maxm = jEvent.pIndex[j][k]
    # print("\t\tmax: %d" % maxm)
    phi_maxm = getPhi(pEvent, maxm)
    eta_maxm = getEta(pEvent, maxm)
    submax = 0
    phi_submax = 0
    eta_submax = 0
    if(len(jEvent.pIndex[j])>1):
        if (maxm == jEvent.pIndex[j][0]):
           submax = jEvent.pIndex[j][1]
        else:
           submax = jEvent.pIndex[j][0]
        for k, index in enumerate(jEvent.pIndex[j]): #finding the particle in the jet with the second highest energy

            if ((pEvent.energy[submax] < pEvent.energy[jEvent.pIndex[j][k]]) and (pEvent.energy[jEvent.pIndex[j][k]] < pEvent.energy[maxm])):
                submax = jEvent.pIndex[j][k]
        # print("\t\tsubmax: %d" % submax)
        # 
        phi_submax = getPhi(pEvent, submax)
        eta_submax = getEta(pEvent, submax)

    return phi_maxm, eta_maxm, phi_submax, eta_submax

def fRotate(jEvent, j, phi, eta, phi_maxm, eta_maxm, phi_submax, eta_submax):
    if(len(jEvent.pIndex[j])>1):
        # print("phi before rotate: %f" % phi)
        # print("phi_maxm to be rotated around: %f" % phi_maxm)
        star = math.atan2((eta_maxm-eta_submax), (phi_maxm-phi_submax))

        alpha = math.atan2(eta,phi) #fill in numbers
        r = math.sqrt(math.pow(phi, 2) + math.pow(eta, 2))
        phi = r * math.cos(alpha-star)
        eta = r * math.sin(alpha-star)

        # print('phi after rotate %f' % phi)



    return phi, eta

def fTranslate(phi, eta, phi_maxm, eta_maxm):
    # print("phi_maxm = %f" % phi_maxm)
    # print("eta_maxm = %f" % eta_maxm)

    # print("phi before translate = %f" % phi)
    # print("eta before translate = %f" % eta)

    phi = phi - phi_maxm
    eta = eta - eta_maxm
    # print("phi after translate = %f" % phi)
    # print("eta after translate = %f\n" % eta)

    return phi, eta

def fReflect_Fill_Print(output, iEvent, jEvent, j, phiTempV, etaTempV, energyTempV, sumEtaPos, sumEtaNeg, histReflect, histJetTemp, collisionType):
    if(len(jEvent.pIndex[j])>1):
 # if(len(jEvent.pIndex[j])>1):
        for i, a in enumerate(etaTempV):
            if(sumEtaPos < sumEtaNeg):
                a = -1*a
        #fill the histogram for reflection
            histReflect.Fill(phiTempV[i], a, energyTempV[i])
        #fill a temporary histogram with data from one jet
            histJetTemp.Fill(phiTempV[i], a, energyTempV[i])

<<<<<<< HEAD
    printOutput(output, j, iEvent, histJetTemp, dimension)
=======
    printOutput(output, j, iEvent, histJetTemp, collisionType)
>>>>>>> 4bd56d7edc09ecefaadffc3d7b1814d5225458cf


    return etaTempV

def fNormalize(jEvent, phiTempV, etaTempV, energyTempV, eTot, histNormalize):
    for i, a in enumerate(etaTempV):
        histNormalize.Fill(phiTempV[i], a, (energyTempV[i]/eTot))
        # if(eTot > 0):
        #     print 'NOTE'
        # else:
            # print 'wut'
    



<<<<<<< HEAD
def readTree(filename1, filename2, fileOut, dimension):
=======
def readTree(filename1, filename2, fileOut, collisionType):
>>>>>>> 4bd56d7edc09ecefaadffc3d7b1814d5225458cf

    fIn = ROOT.TFile(filename1, "READ")
    tree = fIn.Get("tree")
    tree.Print()
    #read in the other tree
    fIn2 = ROOT.TFile(filename2, "READ")
    jetTree = fIn2.Get("jetTree")
    jetTree.Print()

    histBefore = ROOT.TH2F("histBefore", "histBefore", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histBefore.GetXaxis().SetTitle("phi");
    histBefore.GetYaxis().SetTitle("eta");
    histBefore.GetZaxis().SetTitle("counts weighted by energy");

    histCentre = ROOT.TH2F("histCentre", "histCentre", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histCentre.GetXaxis().SetTitle("phi");
    histCentre.GetYaxis().SetTitle("eta");
    histCentre.GetZaxis().SetTitle("counts weighted by energy");

    histRotate = ROOT.TH2F("histRotate", "histRotate", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histRotate.GetXaxis().SetTitle("phi");
    histRotate.GetYaxis().SetTitle("eta");
    histRotate.GetZaxis().SetTitle("counts weighted by energy");

    histTranslate = ROOT.TH2F("histTranslate", "histTranslate", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histTranslate.GetXaxis().SetTitle("phi");
    histTranslate.GetYaxis().SetTitle("eta");
    histTranslate.GetZaxis().SetTitle("counts weighted by energy");

    histReflect = ROOT.TH2F("histReflect", "histReflect", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histReflect.GetXaxis().SetTitle("phi");
    histReflect.GetYaxis().SetTitle("eta");
    histReflect.GetZaxis().SetTitle("counts weighted by energy");

    histJetTemp = ROOT.TH2F("histJetTemp", "histJetTemp", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) # numBins bound bound bin bound bound
    histJetTemp.GetXaxis().SetTitle("phi");
    histJetTemp.GetYaxis().SetTitle("eta");
    histJetTemp.GetZaxis().SetTitle("counts weighted by energy");

    histNormalize = ROOT.TH2F("histNormalize", "histNormalize", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) # numBins bound bound bin bound bound
    histNormalize.GetXaxis().SetTitle("phi");
    histNormalize.GetYaxis().SetTitle("eta");
    histNormalize.GetZaxis().SetTitle("counts weighted by energy");

    canvasBefore = ROOT.TCanvas("canvasBefore", "canvasBefore")
    canvasCentre = ROOT.TCanvas("canvasCentre", "canvasCentre")
    canvasRotate = ROOT.TCanvas("canvasRotate", "canvasRotate")
    canvasTranslate = ROOT.TCanvas("canvasTranslate", "canvasTranslate")
    canvasReflect = ROOT.TCanvas("canvasReflect", "canvasReflect")
    canvasNormalize = ROOT.TCanvas("canvasNormalize", "canvasNormalize")

    iEvent = 0;

    # open('outputC.txt', 'w').close()
    # outputC = open("outputC.txt" , "w" )

    # open('outputR.txt', 'w').close()
    # outputR = open("outputR.txt" , "w" )

    # open('outputT.txt', 'w').close()
    # outputT = open("outputT.txt" , "w" )

    # open('outputF.txt', 'w').close()
    # outputF = open("outputF.txt" , "w" )

    open(fileOut, 'w').close()
    outputN = open(fileOut , "w" )



#LOOP: through each event in tree
    for pEvent, jEvent in  izip(tree, jetTree): #zip

        print("Event %d:" % iEvent)
    #for event in jetTree:
        # print("jEvent.nJets is %d" %jEvent.nJets)
        # print("pEvent.nParticles is %d" %pEvent.nFinalParticles)
#LOOP: through each jet in event    
        for j in range(jEvent.nJets): #j tells you which jet you are in
             
            # print("\tJet number %d" %j)
            # print("\tjEvent.pIndex[j][0] = %d" % jEvent.pIndex[j][0])
            
            phiTempV = []
            etaTempV = []
            energyTempV = []
            sumEtaPos = 0
            sumEtaNeg = 0
            sumEtaZero = 0

            phi_maxm, eta_maxm, phi_submax, eta_submax = findMaxSubmax(jEvent, pEvent, j)
            # print('max phi before centre: %f' % phi_maxm)
            # print('for max:')
            phi_maxm, eta_maxm = fCentre(jEvent, j, phi_maxm, eta_maxm)
            # print('for submax:')
            phi_submax, eta_submax = fCentre(jEvent, j, phi_submax, eta_submax)
            # print('now the rest is about the max: \n')
            # print('phi_max before rotate: %f' % phi_maxm)
            phi_maxR, eta_maxR = fRotate(jEvent, j, phi_maxm, eta_maxm, phi_maxm, eta_maxm, phi_submax, eta_submax)
            # print('phi_max after rotate: %f' % phi_maxR)
            # print('\n')

            for index in (jEvent.pIndex[j]):
                phi, eta = getPhi(pEvent, index), getEta(pEvent, index)
                histBefore.Fill(phi, eta, pEvent.energy[index])
                
                phi, eta = fCentre(jEvent, j, phi, eta)
                histCentre.Fill(phi, eta, pEvent.energy[index])
                #centre the max and submax
                
                phi, eta = fRotate(jEvent, j, phi, eta, phi_maxm, eta_maxm, phi_submax, eta_submax)
                histRotate.Fill(phi, eta, pEvent.energy[index])

                phi, eta = fTranslate(phi, eta, phi_maxR, eta_maxR)
                histTranslate.Fill(phi , eta, pEvent.energy[index])


                if(eta > 0):
                    sumEtaPos += pEvent.energy[index]
                elif(eta < 0):
                    sumEtaNeg += pEvent.energy[index]
                else:
                    sumEtaZero += pEvent.energy[index]
                
                etaTempV.append(eta)
                phiTempV.append(phi)
                energyTempV.append(pEvent.energy[index])
            # print ('sum eta pos: %f' % sumEtaPos)
            # print ('sum eta Neg: %f' % sumEtaNeg)
            # print ('sum eta Zero: %f' % sumEtaZero)
            # print ('sum eta pn: %f' % (sumEtaPos + sumEtaNeg))


            etaTempV = fReflect_Fill_Print(outputN, iEvent, jEvent, j, phiTempV, etaTempV, energyTempV, sumEtaPos, sumEtaNeg, histReflect, histJetTemp, collisionType)
            # print ('sum eta pn: %f' % (sumEtaPos + sumEtaNeg))

            eTot = sumEtaPos + sumEtaNeg + sumEtaZero
            fNormalize(jEvent, phiTempV, etaTempV, energyTempV, eTot, histNormalize)

            etaTempV = []
            phiTempV = []
            energyTempV = []
            histJetTemp.Reset()

            
            # printOutput(outputC, j, iEvent, histCentre, collisionType)
            # printOutput(outputR, j, iEvent, histRotate, collisionType)
            # printOutput(outputT, j, iEvent, histTranslate, collisionType)
            printOutput(outputN, j, iEvent, histNormalize, collisionType)

                
        iEvent+=1


    #see others for examples of iterating through
    # canvasBefore.cd()
    # histBefore.Draw("lego")
    # canvasBefore.SaveAs("before.pdf")

    # canvasCentre.cd()
    # histCentre.Draw("lego")
    # #https://root.cern.ch/root/html534/guides/users-guide/Histograms.html
    # canvasCentre.SaveAs("centre.pdf")

    # canvasRotate.cd()
    # histRotate.Draw("lego")
    # canvasRotate.SaveAs("rotate.pdf")

    # canvasTranslate.cd()
    # histTranslate.Draw("lego")
    # canvasTranslate.SaveAs("translate.pdf")

    # canvasReflect.cd()
    # histReflect.Draw("lego")
    # canvasReflect.SaveAs("reflect.pdf")
    
    # canvasNormalize.cd()
    # histNormalize.Draw("lego")
    # canvasNormalize.SaveAs("normalize.pdf")
    
if __name__ == "__main__":

    filename1 = raw_input("Please provide filename 1 (a .root file from original tree): ")
    filename2 = raw_input("Please provide filename 2 (a .root file after original tree goes through jet finder): ")
<<<<<<< HEAD
    fileOut = raw_input("Please provide an output filename (a .txt file)")

    dimension = raw_input("Enter the side-length of the jet images")

    #filename1 = "ppfileHard.root"
    #filename2 = "jetFile.root"

    readTree(filename1 = filename1, filename2 = filename2, fileOut = fileOut, dimension = dimension)
=======
    fileOut = raw_input("Please provide an output filename (a .txt file): ")
    collisionType = raw_input("Please provide collision type (i.e: pp, pb): ")
    #filename1 = "ppfileHard.root"
    #filename2 = "jetFile.root"

    readTree(filename1 = filename1, filename2 = filename2, fileOut = fileOut, collisionType = collisionType)
>>>>>>> 4bd56d7edc09ecefaadffc3d7b1814d5225458cf


