This readme may be a little in depth compared to most readmes, its length is mostly due to it also sort of functioning as a research writeup, recording how each single piece of the analysis is run.
# Quenched Jet Image Analysis Using Machine Learning
Using computer image recognition techniques to differentiate between samples of jets.[1]
## Getting Started
These instructions will help you set up two machine learning models (LDA and NN) train them on jet images, and extract their discrimination methods. 
### Dependencies
<!-- For installation instructions, select the item -->
- ROOT
- Fastjet[2]
- Tensorflow
- Keras
### Installation
All the jet imaging files can be downloaded by running:
```
git clone https://github.com/brosand/JetStuff.git
```
# Running the code
The jet analysis process contains five steps:
1. [Create event root files](#step-1-create-event-root-files)
2. [Run fastjet to extract the jets](#step-2-run-fastjet-to-extract-the-jets)
3. [Preprocess the jets for training](#step-3-preprocess-the-jets-for-training)
4. [Train the model](#step-4-train-the-model)
5. [Extract the learning from the model](#step-5-extract-the-learning-from-the-model)

For argument help: ```python <prog.py> -h```

## Step 1: Create event root files
We have employed six different methods for creating the initial root files, based on the two formats of data we received, as well as our four different types of simulations.
All of these root trees are of the same format with the name "tree", although some do not have charge and/or mass:
```
tree
├──iEvents
├──nFinalParticles
├──px[]
├──py[]
├──pz[]
├──energy[]
├──charge[]
├──mass[]
```

### Proton pythia generation:
```ppPythia.cpp```
Runs pp collisions using Pythia with a set collision pt minimum of 150 GeV, and stores a tree in the file ```pp.root```

To run:
```
make ppPythiaMake
./ppPythia
```
### W-boson pythia generation:
```wPythia.cpp```
Runs pp collisions in which every event is required to generate a w-boson. It uses Pythia with a set collision pt minimum of 150 GeV, and stores a tree in the file ```w.root```.

To run:
```
make wPythiaMake
./wPythia
```
### Fake lead collision generation:
```leadFake.cpp```
Simulates a lead-lead collision by hand. Tree stored in ```leadFake.root```

To run:
```
make leadFakeMake
./leadFake
```
### Kirill data conversion:
```kirillConvert.cpp```
Converts data from Kirill's four different .dat files into the format of our previous trees, without the charge, which we did not need for our work-- maybe take out. The output root file is stored in ```sampleA.root```, where A is whichever sample is being converted.

To run:
```
>> make kirillConvert.cpp
>> ./kirillConvert.cpp
<< Enter the name of the file to read from (probs a .dat):
// <path to whichever .dat file>
>> folder/sampleA.dat
```

Kirill's four .dat files:
```
Sample A: Radiative losses (soft gluons at large angles)
Sample B: Drag force (these should look very much like vacuum jets except for the energy loss)
Sample C: Modified splitting function
Sampe D: Vacuum pythia6 jets
```
### Li data conversion:
```liConvert.cpp```
Converts data from Li's samples of real STAR data into root files of our established format. The output file is stored in a specified folder with the original name of the file with a "C" before the .root. Note: this tree does not have the branches "iEvents", "nFinalParticles", and charge, but these branches are superfluous. It is also missing "mass", which is much harder to calculate for real data, so will not be utilized to make analysis more precise.
```
file.root folder --> folder/file1C.root
```

To run:
The argument parsing is set up so that both an input file and an output folder must always be inputed.

```
>> make liConvertMake
// ./liConvert <liRootForConversion> <output folder>
>> ./liConvert datafile.root folder
```

In order to move Li's data into a more usable format, all the particle details needed to be moved from the samples into one root file. ```liCombiner.py``` is used for the combination, but all files are hardcoded in. I ran this combiner after converting all the original data. It currently looks in the "Au/AuAu11NPE25" folder for the root files. 

To run:
```
python liCombine.py
```

### PP with noise generation
In order to challenge our models more, we generated pythia pp data with background noise. This program combines the files ```pp.root``` and ```lead.root``` and creates a ```pNoise.root```. The combination is done event by event, so event 1 of ```pp.root``` is added to event 1 of ```lead.root```. The two files are hard coded into the program, but can be changed and re-purposed for combining any two root trees in a similar manner.

To run:
```
python eventCombine.py
```
## Step 2: Run fastjet to extract the jets
We used fastjet to find jets, using an R of 1.0 and cutting at a pt of 120 GeV. The jet finder runs using the anti-kt algorithm, and generates root tree files, which it puts in the designated output folder, with the format:

```
jetTree
├──eventN
├──nJets
├──pIndex[] (of each jet constituent)
├──phi[]     ^^ 
├──eta[]     ^^
├──e[]       ^^
```

To run:
The argument parsing is set up so that all possible arguments must be passed.

```
>> make jetFinderMake
// ./jetFinder <inputFile> <outputFolder> <Jet radius (r)> <pt to cut on(GeV)>
>> ./jetFinder sampleEvents.root folder 1.0 120
```

## Step 3: Preprocess the jets for training
We preprocess the jets so that they all have the same general shape, similar to moving the face for image recognition so that the eyes are always in the same place.
For a detailed visualization, see [our presentation.](https://docs.google.com/presentation/d/1rPWveWBJq7X5Th82QrCt-T69XvCLkd9KctUnCzlCJgg/edit#slide=id.g249b9a98aa_0_208) (slide 7)
To preprocess the jets, we go through five steps:

1. Center the jets

	-For each jet, move the jet so the center of the jet is at 0,0.
2. Rotate the jets

	-For each jet, rotate the jet so that the first and second highest energy(or pt) particle constituents are parallel to the phi axis with the second highest particle on the negative side of the highest particle.
3. Translate the jets

	-Move the whole jet so that the highest particle is at 0,0.
4. Normalize the jets

	-Divide the energy(or pt) of each particle in the jet by the total energy(or pt) of each jet.
5. Reflect the jets

	-If the jet has a higher concentration of energy(or pt) on the negative eta portion of the graph, flip the jet so the the higher concentration is in positive eta space.

These steps are all run in the python program ```prept.py```(for preprocessing based on pt) or ```preEnergy.py```(for preprocessing based on energy). They both take the same several cmd line arguments. The argument parsing is different more my versions instead of Sofia's (Just depending on which file you look at, if you are looking on git, and the file was modified after 8/5/17, it is my version. I didn't want to change hers because her readme is already written and I'm not sure which one you will look at, I just wanted to clean up the arg parsing a bit).
The preprocessing outputs a file as such:
```
Jetfile = "jetFile.root"
Folder = "folder"
Dimension = 10
Preprocessing = 'e'
Output file = Folder/jetFilePre10_e.txt
```
To run:
```
// python pre<pt or Energy>.py --data=<original root event file> --jets=<jet root file> --type=<collision type> --dim=<dimension of jet image> --folder=<folder to place preprocessed jets>
>> python prept.py --data=sampleAEvent.root --jets=sampleAJets.root --type=A --dim=11 --folder=folder
```
We have created several preprocessing scripts, which run on all of Kirill's samples and all our own simulated data. The most updated script is: ```prescriptBen.sh```

## Step 4: Train the model
I will only discuss the neural network here, as Sofia has written up training the LDA.
The two neural networks are a simple fully connected network, and a convolutional network. For a simple diagram explaining the difference, see [this stackexchange post](https://stats.stackexchange.com/questions/114385/what-is-the-difference-between-convolutional-neural-networks-restricted-boltzma)
The fully connected network is run with a Relu activation function, and the final layer is a softmax function. The specific architecture of the CNN can be found in the CNNModel.png file.
To train the network, we need two or more datasets, directly produced by our preprocessing. Any number of data files can be used, but they must each be from a separate class.

To run:
```
// python <NNJet or CNNJet>.py --data=<datafile1> --data=<datafile2>
>> python NNJet.py --data=sampleAPreprocessed.txt --data=sampleBPreprocessed.txt
```
There are other options, such as epochs, layers, for a full list, type ```python NNJet.py -h```

All data from the neural networks, such as accuracy and architecture, is stored in NNData.csv, in addition all networks are saved with a name based on their time of completion and their type. This data can be used to compare with NNData.csv, and rerun the networks for rule extraction. Ideally I would retire this naming convention  as soon as possible, but I don't know if I will have time, so it will probably stick, so far there has been no overlap.

## Step 5: Extract the learning from the model
The principle method that I utilized to extract the neural network's learning was a pearson correlation coefficient, a number calculated based on a dataset and the output for each member of that set. For validation, I also set up a visualization of pixel intensity for different samples, so we could see if the net would learn to look at pixels where we know a difference exists.
### Pixel weights:
```histI.py``` Is right now set up so that it will take an input --data of a sample, then print two histograms, one on a log scale, both of the pixel intensities. The other important inputs are --validation_size and --draw. Draw determines whether a probability distribution will be drawn, or just a histogram of intensity, validation size is the quantity of jets which will be used for the histogram. Classes must also be input, just for the naming of the output file. Finally, the range is the range of the histogram, to help deal with scaling issues, note that bins outside of the range will be treated as if they are at the end of the range. Note that the output folders must be created ahead of time.

```
// python histI.py --data=<"data.txt"> --type=<type>
// Using TensorFlow backend.
// Info in <TCanvas::Print>: pdf file coeffs<validation_size>/r<range>/<type>_<dimension>.pdf has been created
>> python histI.py --data="sampleA21.txt" --type=A
<< Using TensorFlow backend.
>> Info in <TCanvas::Print>: pdf file coeffs1000/r1.0/A_11.pdf has been created
```
### Pearson correlation coefficient:
More details about the math can be found in [the wikipedia article.](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient)
```pearsonCalc.py``` also takes a validation size, and runs on a specific NN model, and both the model weights and architecture need to be specified.
Pearson histogram pdf created in ```pearson/<validation_size>/<classes>_<dimension>_NNPearsonCoeff.pdf```
Warning: to run on CNN, change the name so pdfs not overwritten.
This pdf is a map of how correlated the intensity of each pixel is with the output. Positive values signify a correlation with the the first sample in the neural network, negative values signify a correlation with the second sample. Default validation size is 10,000; I reccomend you change it to however many data samples you are working with, the more samples the more effective the program becomes. Note: This program is not designed for more than two classes.

To run:
```
// python pearsonCalc.py --data=<PreprocessedJets.txt> --classes=<neural net classes> --weights=<net weights> --architecture=<model architecture>
>> python pearsonCalc.py --data=sampleA.txt --classes=AB --weights=ABNeuralNetWeights.h5 --architecture=ABNeuralNetModel.json
```

## Notes
Anything in the folder ```old``` may not be accurate, particularly the NNData.csv.


[1] Jet Image machine learning analysis inspired by: Luke de Oliveira, Michael Kagan, Lester Mackey, Benjamin Nachman, Ariel Schwartzman; arXiv:1511.05190 [hep-ph]

[2] Fastjet: M. Cacciari, G.P. Salam and G. Soyez, Eur.Phys.J. C72 (2012) 1896 [arXiv:1111.6097]
