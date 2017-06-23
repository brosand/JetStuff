import ROOT
import fastjet
import array

def findJet(filename):
    fIn = ROOT.TFile(filename, 'READ')
    tree = fIn.Get('tree')

    #TTreeReader declaration
    myReader = TTreeReader('tree', f)
    # myPx = TTreeReaderArray(myReader, "px")
    # myPy = TTreeReaderArray(myReader, "py")
    # myPz = TTreeReaderArray(myReader, "pz")
    # myEnergy = TTreeReaderArray(myReader, "energy")
    # myEvents = TTreeReaderrValue(myReader, "iEvents")
    # myNFinalParticles = TTreeReaderValue(myReader, "nFinalParticles")

    #double check that the while and its containers shouldn't be further out
   
    #output objects
        #nEvent Change!
        #nEvent = tree.iEvents
    pt = []
    #y = rapidity
    y = []
    phi = []

    #create output TTree
    jetTree = TTree('jetTree', 'ttree with jet data')
    tree.branch('eventN', &nEvent, 'eventN/I')
    tree.branch('nJets', &nJets, 'nJets/I')
    tree.Branch("pt", &pt);
    tree.Branch("y", &y);
    tree.Branch("phi", &phi);

#loop through tree and turn particles into pseudojets
    for event in tree
        for particle in event
            particles = []
            particles.push_back(PseudoJet(particle.px, particle.py, particle.pz, particle.energy))
 
    #choose a jet definition
        R = 0.6

        Jet_def = JetDefinition(antikt_algorithm, R)
    #run the clustering, extract the jets
        cs = ClusterSequence(particles)
        #is 32 necessary?
        jets = vector(PseudoJet)
        jets = sorted_by_pt(cs.inclusive_jets())


    #fill output TTree
        for i in jets 
            pt.append(jets[i].pt)
            phi.append(jets[i].phi)
            y.append(jets[i].rap)


    #quasi-main
    if __name__ == '__main__':
    filename = 'ppfile.root'
    readTree(filename = filename)

    ##--> import fastjet prob won't work