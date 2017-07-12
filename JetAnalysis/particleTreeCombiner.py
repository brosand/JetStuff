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

    maxn=0 #Problem: have to go through both trees twice, first to count for length of array
    for e1, e2 in izip(tree1,tree2):
         maxn+= (tree1.nFinalParticles + tree2.nFinalParticles)

    iEvents = array('i', [0])
    nFinalParticles = array('i', [0])
    pt = array('f', maxn*[0.])
    px = array('f', maxn*[0.])
    py = array('f', maxn*[0.])
    pz = array('f', maxn*[0.])
    charge = array('f', maxn*[0.])
    mass = array('f', maxn*[0.])
    energy = array('f', maxn*[0.])


    #works best with trees with same length
    #create the output tree
    tree = TTree('tree', 'tree with event data and particle data in arrays')
    tree.Branch('iEvents', iEvents, 'iEvents/I');
    tree.Branch('nFinalParticles', nFinalParticles, 'nFinalParticles/I');
    # tree.Branch('pt', pt, 'pt[nFinalParticles]/D');
    tree.Branch('px', px, 'px[nFinalParticles]/F');
    tree.Branch('py', py, 'py[nFinalParticles]/F');
    tree.Branch('pz', pz, 'pz[nFinalParticles]/F');
    # tree.Branch('charge', charge, 'charge[nFinalParticles]/I');
    # tree.Branch('mass', mass, 'mass[nFinalParticles]/F');
    tree.Branch('energy', energy, 'energy[nFinalParticles]/F');



    for aEvent, bEvent in izip(tree1, tree2):
        iEvents[0] = aEvent.iEvents
        nFinalParticles[0] = (aEvent.nFinalParticles + bEvent.nFinalParticles)
        px.extend(aEvent.px)
        px.extend(bEvent.px)
        py.extend(aEvent.py)
        py.extend(bEvent.py)
        pz.extend(aEvent.pz)
        pz.extend(bEvent.pz)
        energy.extend(aEvent.energy)
        energy.extend(bEvent.energy)
    tree.Fill()
    fOut.Write()

    fOut.Close()
    print 'combination successful'


if __name__ == "__main__":

    # filename1 = raw_input("Please provide filename 1 (a .root file from tree1): ")
    # filename2 = raw_input("Please provide filename 2 (a .root file from tree2): ")

    # fileOut = raw_input("Please provide an output filename (a .root file):")

    rootCombine(file1='pp.root',file2='lead.root', fileOut='t.root')

