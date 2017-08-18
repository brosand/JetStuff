#input: a tree with all the particle data, a tree with all the jet data
#output: a tree where for each event, one branch for event number, one branch for number of jets, one branch is a vector of vectors containing the indices of each particle within a jet. This way with these indices we can go back to the tree and get information about these jets
from itertools import izip
import ROOT
import array
import numpy as np
import math
from PIL import Image
import sys
import argparse

HIST_BOUND = 1.0

def getDimension():
    dimension = input("Enter the side-length of the jet images: ")
    return dimension

def printOutput(output, j, iEvent, histogram, dimension,  collisionType):
    # im = Image.new("RGB", (dimension, dimension))
    # pix = im.load()

    output.write(collisionType)
    output.write(" %d" % dimension)
    for q in range(dimension):
        for r in range(dimension):
            output.write(" %f" % histogram.GetBinContent(q + 1, r + 1))
            # pix[q,r] = (int(histogram.GetBinContent(q+1, r+1)*256),0,0)
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
    # print("JUST FOR KICKS:")
    # print("phi: %f" % phi)
    # print("phijet: %f" % phijet)
    phi = phi-phijet
    # print("new phi: %f" % phi)
    while(phi < -math.pi):
        phi += 2*math.pi
    while(phi > math.pi):
        phi -= 2*math.pi
    # print("new again phi: %f" % phi)
    eta = eta-etajet
    # print('phi after centre: %f' % phi)

    return phi, eta

def findMaxSubmax(jEvent, pEvent, j, histsubmaxcheck):
    maxm = jEvent.pIndex[j][0]

    for k, index in enumerate(jEvent.pIndex[j]):
#index will give the particle index, eg [7, 21, 32], k gives 0, 1, 2
        # print("\t\t\tpt[%d] = %f" % (jEvent.pIndex[j][k], pEvent.pt[jEvent.pIndex[j][k]]))
        #events[0].pt[event[1].pIndex[j][k]] #how to tap into event number on other tree
        #tree.event.pt[event.pIndex[j][k]] #how to tap into event number on other tree
         
        #finding the particle in the jet with the highest pt
        if pEvent.pt[jEvent.pIndex[j][k]] > pEvent.pt[maxm]:
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
        for k, index in enumerate(jEvent.pIndex[j]): #finding the particle in the jet with the second highest pt

            if ((pEvent.pt[submax] < pEvent.pt[jEvent.pIndex[j][k]]) and (pEvent.pt[jEvent.pIndex[j][k]] < pEvent.pt[maxm])):
                submax = jEvent.pIndex[j][k]
        # print("\t\tsubmax: %d" % submax)
        # 
        phi_submax = getPhi(pEvent, submax)
        eta_submax = getEta(pEvent, submax)

    # print("pt[maxm] for jet %d: %f" % (k, pEvent.pt[maxm]))
    # print("pt[submax] for jet %d: %f" % (k, pEvent.pt[submax]))


    histsubmaxcheck.Fill(pEvent.pt[maxm], pEvent.pt[submax])

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

def fReflect_Fill_Print(output, iEvent, jEvent, j, phiTempV, etaTempV, ptTempV, sumEtaPos, sumEtaNeg, histReflect, histJetTemp, collisionType):
    if(len(jEvent.pIndex[j])>1):
 # if(len(jEvent.pIndex[j])>1):
        for i, a in enumerate(etaTempV):
            if(sumEtaPos < sumEtaNeg):
                a = -1*a
        #fill the histogram for reflection
            histReflect.Fill(phiTempV[i], a, ptTempV[i])
        #fill a temporary histogram with data from one jet
            histJetTemp.Fill(phiTempV[i], a, ptTempV[i])

    printOutput(output, j, iEvent, histJetTemp, dimension, collisionType)

    return etaTempV

def fNormalize(ptTempV):
    outVector = []
    ptSum = np.sum(ptTempV)
    for i in ptTempV:
        outVector.append(i/ptSum)
    return outVector

    # for i, a in enumerate(etaTempV):
    #     histNormalize.Fill(phiTempV[i], a, (ptTempV[i]/eTot))
    # return histNormalize

        # if(eTot > 0):
        #     print 'NOTE'
        # else:
            # print 'wut'

def readTree(filename1, filename2, fileOut, dimension, collisionType, folder):

    fIn = ROOT.TFile(filename1, "READ")
    tree = fIn.Get("tree")
    tree.Print()
    #read in the other tree
    fIn2 = ROOT.TFile(filename2, "READ")
    jetTree = fIn2.Get("jetTree")
    jetTree.Print()

    histBefore = ROOT.TH2F("histBefore", "histBefore", dimension, -2*math.pi, 2*math.pi, dimension, -5, 5) #bin bound bound bin bound bound
    histBefore.GetXaxis().SetTitle("phi");
    histBefore.GetYaxis().SetTitle("eta");
    histBefore.GetZaxis().SetTitle("counts weighted by pt");

    histCentre = ROOT.TH2F("histCentre", "histCentre", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histCentre.GetXaxis().SetTitle("phi");
    histCentre.GetYaxis().SetTitle("eta");
    histCentre.GetZaxis().SetTitle("counts weighted by pt");

    histRotate = ROOT.TH2F("histRotate", "histRotate", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histRotate.GetXaxis().SetTitle("phi");
    histRotate.GetYaxis().SetTitle("eta");
    histRotate.GetZaxis().SetTitle("counts weighted by pt");

    histTranslate = ROOT.TH2F("histTranslate", "histTranslate", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histTranslate.GetXaxis().SetTitle("phi");
    histTranslate.GetYaxis().SetTitle("eta");
    histTranslate.GetZaxis().SetTitle("counts weighted by pt");

    histReflect = ROOT.TH2F("histReflect", "histReflect", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) #bin bound bound bin bound bound
    histReflect.GetXaxis().SetTitle("phi");
    histReflect.GetYaxis().SetTitle("eta");
    histReflect.GetZaxis().SetTitle("counts weighted by pt");

    histJetTemp = ROOT.TH2F("histJetTemp", "histJetTemp", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) # numBins bound bound bin bound bound
    histJetTemp.GetXaxis().SetTitle("phi");
    histJetTemp.GetYaxis().SetTitle("eta");
    histJetTemp.GetZaxis().SetTitle("counts weighted by pt");

    histsubmaxcheck = ROOT.TH2F("histsubmaxcheck", "histsubmaxcheck", dimension, 0, 100, dimension, 0, 100) # numBins bound bound bin bound bound
    histsubmaxcheck.GetXaxis().SetTitle("pt of max");
    histsubmaxcheck.GetYaxis().SetTitle("pt of submax");
    histsubmaxcheck.GetZaxis().SetTitle("counts");

    # histNormalize = ROOT.TH2F("histNormalize", "histNormalize", dimension, -HIST_BOUND, HIST_BOUND, dimension, -HIST_BOUND, HIST_BOUND) # numBins bound bound bin bound bound
    # histNormalize.GetXaxis().SetTitle("phi");
    # histNormalize.GetYaxis().SetTitle("eta");
    # histNormalize.GetZaxis().SetTitle("counts weighted by pt");

    canvasBefore = ROOT.TCanvas("canvasBefore", "canvasBefore")
    canvasCentre = ROOT.TCanvas("canvasCentre", "canvasCentre")
    canvasRotate = ROOT.TCanvas("canvasRotate", "canvasRotate")
    canvasTranslate = ROOT.TCanvas("canvasTranslate", "canvasTranslate")
    canvasReflect = ROOT.TCanvas("canvasReflect", "canvasReflect")
    canvasSubmaxCheck = ROOT.TCanvas("canvasSubmaxCheck", "canvasSubmaxCheck")
    # canvasNormalize = ROOT.TCanvas("canvasNormalize", "canvasNormalize")

    iEvent = 0

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
        # if (iEvent==1):
        #     break
        if (iEvent % 100 == 0):
            print("Event %d:" % iEvent)
    #for event in jetTree:
        # print("jEvent.nJets is %d" %jEvent.nJets)
        # print("pEvent.nParticles is %d" %pEvent.nFinalParticles)
#LOOP: through each jet in event    
        for j in range(jEvent.nJets): #j tells you which jet you are in
            # print("This is what j is: ")
            # print(j)
            # if(j == 1):
                # break

            # print("\tJet number %d" %j)
            # print("\tjEvent.pIndex[j][0] = %d" % jEvent.pIndex[j][0])
            
            phiTempV = []
            etaTempV = []
            ptTempV = []
            sumEtaPos = 0
            sumEtaNeg = 0
            sumEtaZero = 0

            phi_maxm, eta_maxm, phi_submax, eta_submax = findMaxSubmax(jEvent, pEvent, j, histsubmaxcheck)
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

                histBefore.Fill(phi, eta, pEvent.pt[index])
                
                phi, eta = fCentre(jEvent, j, phi, eta)
                histCentre.Fill(phi, eta, pEvent.pt[index])
                #centre the max and submax
                
                phi, eta = fRotate(jEvent, j, phi, eta, phi_maxm, eta_maxm, phi_submax, eta_submax)
                histRotate.Fill(phi, eta, pEvent.pt[index])

                phi, eta = fTranslate(phi, eta, phi_maxR, eta_maxR)
                histTranslate.Fill(phi , eta, pEvent.pt[index])


                if(eta > 0):
                    sumEtaPos += pEvent.pt[index]
                elif(eta < 0):
                    sumEtaNeg += pEvent.pt[index]
                else:
                    sumEtaZero += pEvent.pt[index]
                
                etaTempV.append(eta)
                phiTempV.append(phi)
                ptTempV.append(pEvent.pt[index])
            # print ('sum eta pos: %f' % sumEtaPos)
            # print ('sum eta Neg: %f' % sumEtaNeg)
            # print ('sum eta Zero: %f' % sumEtaZero)
            # print ('sum eta pn: %f' % (sumEtaPos + sumEtaNeg))

            ptTempV = fNormalize(ptTempV)
            # print 'len pt'
            # print len(ptTempV)
            # print ptTempV[21]
            etaTempV = fReflect_Fill_Print(outputN, iEvent, jEvent, j, phiTempV, etaTempV, ptTempV, sumEtaPos, sumEtaNeg, histReflect, histJetTemp, collisionType)
            # print ('sum eta pn: %f' % (sumEtaPos + sumEtaNeg))

            # eTot = sumEtaPos + sumEtaNeg + sumEtaZero
            # histNormalize = fNormalize(jEvent, phiTempV, etaTempV, ptTempV, eTot, histNormalize, dimension, collisionType)

            etaTempV = []
            phiTempV = []
            ptTempV = []
            histJetTemp.Reset()


            
            # printOutput(outputC, j, iEvent, histCentre, dimension, collisionType)
            # printOutput(outputR, j, iEvent, histRotate, dimension, collisionType)
            # printOutput(outputT, j, iEvent, histTranslate, dimension, collisionType)
            # printOutput(outputN, j, iEvent, histNormalize, dimension, collisionType)
            # printOutput(outputN, j, iEvent, histReflect, dimension, collisionType)
# 
                
        iEvent+=1


    #see others for examples of iterating through
    canvasBefore.cd()
    histBefore.Draw("LEGO2Z")
    canvasBefore.SaveAs(folder + "/" + filename1.split('.')[0] + "_" + str(dimension) + "_before_pt.pdf")

    canvasCentre.cd()
    # canvasCentre.SetLogz()
    histCentre.Draw("LEGO2Z")
    #https://root.cern.ch/root/html534/guides/users-guide/Histograms.html
    canvasCentre.SaveAs(folder + "/" + filename1.split('.')[0] + "_" + str(dimension) + "_centre_pt.pdf")

    canvasRotate.cd()
    # canvasRotate.SetLogz()
    histRotate.Draw("LEGO2Z")
    canvasRotate.SaveAs(folder + "/" + filename1.split('.')[0] + "_" + str(dimension) + "_rotate_pt.pdf")

    canvasTranslate.cd()
    # canvasTranslate.SetLogz()
    histTranslate.Draw("LEGO2Z")
    canvasTranslate.SaveAs(folder + "/" + filename1.split('.')[0] + "_" + str(dimension) + "_translate_pt.pdf")

    canvasReflect.cd()
    # canvasReflect.SetLogz()
    histReflect.Draw("LEGO2Z")
    canvasReflect.SaveAs(folder + "/" + filename1.split('.')[0] + "_" + str(dimension) + "_reflect_pt.pdf")

    canvasSubmaxCheck.cd()
    histsubmaxcheck.Draw("LEGO2Z")
    canvasSubmaxCheck.SaveAs(folder + "/" + filename1.split('.')[0] + "_" + str(dimension) + "_submaxCheck_pt.pdf")
    
    # canvasNormalize.cd()
    # histNormalize.Draw("LEGO2Z")
    # canvasNormalize.SaveAs("normalize.pdf")
    
if __name__ == "__main__":

    
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='sampleA.root', help='the original root file of event data')
    parser.add_argument('--jets', default='r1.0/sampleAJet.root', help='the original root file of event data')
    parser.add_argument('--type', default='A', help='type of collision(collision ID)')
    parser.add_argument('--dim', default='11', help='dimension of output image', type=int)
    parser.add_argument('--folder', default='r1.0', help='folder to place output image')
    args = parser.parse_args()
    
    filename1=args.data
    filename2=args.jets
    dimension=args.dim
    folder=args.folder
    collisionType=args.type

    if(filename1 == ""):
        filename1 = raw_input("Please provide filename 1 (a .root file from original tree): ")
    if(filename2 == ""):
        filename2 = raw_input("Please provide filename 2 (a .root file after original tree goes through jet finder): ")
    if(collisionType == ""):
        collisionType = raw_input("Enter the collision type: ")
    if (dimension == 0):
        dimension = getDimension()
    if(folder == ""):
        folder = raw_input("Please provide folder where you would like everything to go: ")

#give tree, jettree, output txt, collisiontype= , dimension=         

    fileOut = folder + "/" + filename2.split('/')[1].split('.')[0] + "Pre" + str(dimension) + "_pt.txt"
    print("fileOut: %s" % fileOut)
    print("filename2: %s" % filename2)


    print("folder: %s" % folder)

    readTree(filename1 = filename1, filename2 = filename2, fileOut = fileOut, dimension = dimension, collisionType = collisionType, folder = folder)
    


