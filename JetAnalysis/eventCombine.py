from rootpy.tree import Tree, TreeModel
from rootpy.tree import IntCol, DoubleArrayCol
from rootpy.io import root_open
from ROOT import TFile
from itertools import izip

ARRAY_LENGTH = 2100

class Event(TreeModel):
    # def __init__(self):
        iEvents = IntCol()
        nFinalParticles = IntCol()
        # num_vals = IntCol()
        px = DoubleArrayCol(ARRAY_LENGTH)
        py = DoubleArrayCol(ARRAY_LENGTH)
        pz = DoubleArrayCol(ARRAY_LENGTH)
        energy = DoubleArrayCol(ARRAY_LENGTH)
        # TreeModel.__init__(self)

def rootCombine(file1, file2, fileOut):


    fIn = TFile(file1, 'READ')
    tree1 = fIn.Get('tree') #ONLY FOR TREES NAMED TREE

    fIn2 = TFile(file2, 'READ')
    tree2 = fIn.Get('tree') #ONLY FOR TREES NAMED TREE

    # fOut = TFile(fileOut, "recreate")

    fOut = root_open(fileOut, 'recreate')



    tree = Tree('tree', model = Event)
    # tree.num_vals = 120
    # print tree.num_vals
    ctr = 0
    for aEvent, bEvent in izip(tree1, tree2):
        ctr += 1
        if (ctr % 100 == 0):
            print('Event: %d' %ctr)
        tree.iEvents = aEvent.iEvents
        tree.nFinalParticles = (aEvent.nFinalParticles + bEvent.nFinalParticles)
        if (tree.nFinalParticles > ARRAY_LENGTH):
            print ('event: %d contains too many particles: %d' %(aEvent.iEvents, tree.nFinalParticles))
            break
        for i in range(aEvent.nFinalParticles):
            # print aEvent.px[i]
            tree.px[i] = aEvent.px[i]
            tree.py[i] = aEvent.py[i]
            tree.pz[i] = aEvent.pz[i]
            tree.energy[i] = aEvent.energy[i]
            # tree.num_vals+=1


        for i in range(bEvent.nFinalParticles):
            tree.px[aEvent.nFinalParticles + i] = bEvent.px[i]
            tree.py[aEvent.nFinalParticles + i] = bEvent.py[i]
            tree.pz[aEvent.nFinalParticles + i] = bEvent.pz[i]
            tree.energy[aEvent.nFinalParticles + i] = bEvent.energy[i]
            # tree.num_vals+=1

        tree.fill()
    fOut.write()

    tree.px.reset()
    tree.py.reset()
    tree.pz.reset()
    tree.energy.reset()
    # tree.csv()
    fOut.close()
    print 'Done'


        # tree.px.extend(bEvent.px)
        # tree.py.extend(bEvent.py)

        # tree.pz.extend(bEvent.pz)

        # tree.energy.extend(bEvent.energy)
        # print nParticles
        # print px
        # print len(px)
    


if __name__ == "__main__":

    # filename1 = raw_input("Please provide filename 1 (a .root file from tree1): ")
    # filename2 = raw_input("Please provide filename 2 (a .root file from tree2): ")

    # fileOut = raw_input("Please provide an output filename (a .root file):")

    rootCombine(file1='pp.root',file2='lead.root', fileOut='pNoise.root')

