#this will create an identical txt file except now everything is uniform

import math

DIMENSION_JET_IMAGE = 3
COLLISION_TYPE = "UniformDecoy"
nEvents = 10
nJets = 50

def printOutput(output, j, iEvent):

    decoy = 1/(math.pow(DIMENSION_JET_IMAGE, 2))
    print(decoy)

    output.write(COLLISION_TYPE)
    for q in range(DIMENSION_JET_IMAGE):
        for r in range(DIMENSION_JET_IMAGE):
            output.write(" %f  " % decoy)
    output.write(" %d %d \n" % (j, iEvent))

if __name__ == "__main__":

    open('outputUniformDecoy.txt', 'w').close()
    output = open("outputUniformDecoy.txt" , "w" )

    for iEvent in range(nEvents):
        for j in range(nJets): 

            printOutput(output, j, iEvent)
