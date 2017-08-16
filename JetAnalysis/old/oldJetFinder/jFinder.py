import ROOT
import os
ROOT.gInterpreter.AddIncludePath(os.path.join(os.environ["FASTJET_ROOT"], "include"))
ROOT.gInterpreter.ProcessLine('#include "fastjet/PseudoJet.hh"')
ROOT.gInterpreter.ProcessLine('#include "fastjet/ClusterSequenceArea.hh"')
ROOT.gInterpreter.ProcessLine('#include "fastjet/JetDefinition.hh"')
ROOT.gInterpreter.ProcessLine('#include "fastjet/AreaDefinition.hh"')
ROOT.gSystem.Load('libfastjet')
import ROOT.fastjet as fj
from array import array

def findJet(filename):
    fIn = ROOT.TFile(filename, 'READ')
    tree = fIn.Get('tree')

  
    #output vectors for the tree

    eventN = array('i', [0])
    nJets = array('i', [0])
    pIndex = array('i', [0])

    #create output TTree
    jetTree = ROOT.TTree('jetTree', 'ttree with jet data')
    jetTree.Branch('eventN', eventN, 'eventN/I')
    jetTree.Branch('nJets', nJets, 'nJets/I')
    jetTree.Branch('pIndex', pIndex, 'pIndex/I')
    

#loop through tree and turn particles into pseudojets
    for event in tree:
    	print('test1')    
    	uIndex = 0
        iEvent = 0
        particles = []
        for particle in event:
            for p in zip(particle.px, particle.py, particle.pz, particle.energy):
                pjet = fj.PseudoJet(p[0], p[1], p[2], p[3])
                pjet.set_user_index(uIndex)
                particles.append(pjet)
            	uIndex+=1
 
    #choose a jet definition and area definition
        R = 0.6

        jet_def = fj.JetDefinition(fj.antikt_algorithm, R)
        area_def = fj.AreaDefinition(fj.voronoi_area)
    #run the clustering, extract the jets
#, jet_def, area_def
        #is 32 necessary?
        jets = []
        cs = fj.ClusterSequenceArea(particles)
        jets = fj.sorted_by_pt(cs.inclusive_jets())

        nJets.append(len(jets))
        eventN.append(iEvent)
        eventN +=1


    #fill output TTree
        for j in jets:
        	ptemp = []
        	for ptl in j: 
	            pTemp.append(jets[i].user_index())
	        pIndex.append(ptemp)

    	jetTree.Fill()


    jetTree.Print()

    f = ROOT.TFile("jetFile.root", "recreate")
    jetTree.Write()

    f.Close()
    #quasi-main
if __name__ == '__main__':
    # filename = 'ppfile.root'
    findJet(filename = 'ppfile.root')

    ##--> import fastjet prob won't work