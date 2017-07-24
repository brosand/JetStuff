from ROOT import TFile, TTree
from itertools import izip
from array import array

def rootCombine(file1, file2, fileOut):
    # h = TH1F( 'h1', 'test', 100, -10., 10. )

    fIn = TFile(file1, 'READ')
    tree1 = fIn.Get('tree') #ONLY FOR TREES NAMED TREE

    fIn2 = TFile(file2, 'READ')
    tree2 = fIn.Get('tree') #ONLY FOR TREES NAMED TREE

    fOut = TFile(fileOut, "recreate")

    #Declaration of variables for the output tree

    # maxn=1 #Problem: have to go through both trees twice, first to count for length of array
    # for e1, e2 in izip(tree1,tree2):
    #      if ((e1.nFinalParticles + e2.nFinalParticles) > maxn):
    #         maxn = e1.nFinalParticles + e2.nFinalParticles

    iEvents = 0 #array('i')
    nParticles = 0#array('i')
    # nFinalParticles[0] = 10000
    # pt = array('d', maxn*[])
    px = array('f')
    py = array('f')
    pz = array('f')
    charge = array('f')
    mass = array('f')
    energy = array('f')


    #works best with trees with same length
    #create the output tree
    tree = TTree('tree', 'tree with event data and particle data in arrays')
    tree.Branch('iEvents', iEvents, 'iEvents/I');
    tree.Branch('nFinalParticles', nParticles, 'nFinalParticles/I');
    # tree.Branch('pt', pt, 'pt[nFinalParticles]/D');
    tree.Branch('px', px, 'px[1100]/F');
    tree.Branch('py', py, 'py[1100]/F');
    tree.Branch('pz', pz, 'pz[1100]/F');
    tree.Branch('energy', energy, 'energy[1100]/F');
    # tree.Branch('charge', charge, 'charge[nFinalParticles]/I');
    # tree.Branch('mass', mass, 'mass[nFinalParticles]/D');



    for aEvent, bEvent in izip(tree1, tree2):
        iEvents = aEvent.iEvents
        nParticles = (aEvent.nFinalParticles + bEvent.nFinalParticles)
        px.extend(aEvent.px)
        # px.extend(bEvent.px)
        py.extend(aEvent.py)
        # py.extend(bEvent.py)
        pz.extend(aEvent.pz)
        # pz.extend(bEvent.pz)
        energy.extend(aEvent.energy)
        # energy.extend(bEvent.energy)
        print nParticles
        # print px
        tree.Fill()
        print len(px)
        px = []
        py = []
        pz = []
        energy = []
    fOut.Write()

    fOut.Close()
    print 'combination successful'


if __name__ == "__main__":

    # filename1 = raw_input("Please provide filename 1 (a .root file from tree1): ")
    # filename2 = raw_input("Please provide filename 2 (a .root file from tree2): ")

    # fileOut = raw_input("Please provide an output filename (a .root file):")

    rootCombine(file1='pp.root',file2='lead.root', fileOut='combine.root')

