#this will create an identical txt file except now everything is 0s

DIMENSION_JET_IMAGE = 3
COLLISION_TYPE = "ZeroDecoy"
DECOY = 0
nEvents = 10
nJets = 50

def printOutput(output, j, iEvent):

    output.write(COLLISION_TYPE)
    for q in range(DIMENSION_JET_IMAGE):
        for r in range(DIMENSION_JET_IMAGE):
            output.write(" %f" % DECOY)
<<<<<<< HEAD
    output.write(" %d %d\n" % (j, iEvent))
=======
    output.write(" %d %d \n" % (j, iEvent))
>>>>>>> 9f4b858e09e9427c299b5dc110699a7156cdb12d

if __name__ == "__main__":

    open('outputZeroDecoy.txt', 'w').close()
    output = open("outputZeroDecoy.txt" , "w" )

    for iEvent in range(nEvents):
        for j in range(nJets): 

            printOutput(output, j, iEvent)
