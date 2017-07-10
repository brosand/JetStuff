# Linking pythia to fastjet ( Adapted form Vincia1024 makefile and Dr. Soyez's tutorial)
# test OS - Ubuntu 11.04 64bit;
# Mushfiq, University of Dhaka , date : 06.11.2011 .
#Now Checa edits
#now this can be a generic version in the home directory


SHELL = /bin/sh
TOPDIR=$(shell \pwd)

#deal with root
ROOTDIR = /home/yu.yale.edu/sc2554/sw/root/install
#ROOTFLAGS = -I$(ROOTDIR)/include
ROOTFLAGS =$(shell \root-config --cflags)
ROOTLIBS =$(shell \root-config --libs)
#ROOTLIBS = -L$(ROOTDIR)/lib -lCore \
#         -lGraf -lGraf3d -lHist -lHtml -#lMatrix -lMinuit \
#         -lPostscript -lProof -lTree \
#         -lGpad -lGui -lGX11 -lRint \
#         -L/usr/lib/X11R5 -lXpm  -lX11 -lm -lMathCore 
#what-l do I need for ROOTLIBS


# deal with pythia 
#PYTHIADIR = its your local path to pythia. In my case its in the same directory
#where this Makefile is placed
PYTHIADIR   = /home/yu.yale.edu/sc2554/root/pythia/pythia8226
PYTHIAFLAGS = -I$(PYTHIADIR)/include 
PYTHIALIBS  =  -L$(PYTHIADIR)/lib/ -lpythia8
# -llhapdfdummy


# Include Pythia and Pythia examples config files
-include $(PYTHIADIR)/config.mk
-include $(PYTHIADIR)/examples/config.mk


# deal with fastjet
#FASTJETDIR = your local path to fastjet. 

FASTJETDIR  = /home/yu.yale.edu/br384/fastjet-install
FASTJETINC :=`$(FASTJETDIR)/bin/fastjet-config --cxxflags --plugins`
FASTJETLIB :=`$(FASTJETDIR)/bin/fastjet-config --libs --plugins`

# LHAPDF if you want to replace Pythia's dummy default
LHAPDFARGS =
#LHAPDFARGS = -L$(HOME)/local/lib -lLHAPDF -I$(HOME)/local/include

# main61.cc in the example folder uses fastjet. Put this in the same folder
# where the make file is placed. 
clean:
	 rm -f $(obj) 
lead:

	g++ -o lead leadtree3.cpp $(PYTHIAFLAGS) $(PYTHIALIBS) $(FASTJETINC) $(FASTJETLIB) $(LHAPDFARGS) $(ROOTFLAGS) $(ROOTLIBS) -lTreePlayer loader_C.so

pp:

	g++ -o test2 test2.cpp $(PYTHIAFLAGS) $(PYTHIALIBS) $(FASTJETINC) $(FASTJETLIB) $(LHAPDFARGS) $(ROOTFLAGS) $(ROOTLIBS) -lTreePlayer loader_C.so

all:
	g++ -o jetFind jFinder2.cpp $(PYTHIAFLAGS) $(PYTHIALIBS) $(FASTJETINC) $(FASTJETLIB) $(LHAPDFARGS) $(ROOTFLAGS) $(ROOTLIBS) -lTreePlayer loader_C.so





