import ROOT
import sys
lista = ["r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_C_0-99CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_300-349_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_650-699_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_C_100-199CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_300-349_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_650-699CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_0-99_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_300-349CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_700-749_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_0-99_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_350-399_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_700-749_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_0-99_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_350-399_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_700-749_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_0-99_4CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_350-399_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_700-749CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_0-99_5CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_350-399CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_750-799_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_0-99_6CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_400-449_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_750-799_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_0-99CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_400-449_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_750-799CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_100-149_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_400-449_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_800-849_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_100-149_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_400-449CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_800-849_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_100-149CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_450-499_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_800-849_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_150-199_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_450-499_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_800-849CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_150-199_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_450-499CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_850-899_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_150-199_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_500-549_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_850-899_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_150-199CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_500-549_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_850-899_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_200-249_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_500-549CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_850-899CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_200-249_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_550-599_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_900-949_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_200-249_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_550-599_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_900-949_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_200-249CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_550-599CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_900-949CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_250-299_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_600-649_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_950-999_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_250-299_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_600-649_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_950-999_2CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_250-299_3CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_600-649CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_950-999CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_250-299CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_650-699_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_300-349_1CJet.root",
"r0.2/Au/AuAu11NPE25/Small_AuAu11Pico_D_650-699_2CJet.root"]

ch = ROOT.TChain("jetTree")
ctr = 0
for i in lista:
    ch.Add(i)
    ctr +=1
    sys.stdout.write("\rAdded tree %d" % ctr)
    sys.stdout.flush()
ch.Merge("bigJet.root")
print('\nMerge Complete')
