from libPython.tnpClassUtils import tnpSample

eosSOSMuon2018 = "/eos/user/k/kpanos/genproductions/displaced_sos/NANOAODSIM/"

SOS_Muon_2018 = {
#    "DY"   : tnpSample("DY"     , eosSOSMuon2018 + "production_161122_muonSF_tnpTrees_dy/DYJetsToLL_M50_HT1200to2500.root"  , isMC = True, nEvts =  -1 ),
    "DY"   : tnpSample("DY"     , eosSOSMuon2018 + "production_081222_muonSF_tnpTrees_dyFull/test/DYJetsToLL_M50_aMC_part*.root"  , isMC = True, nEvts =  -1 ),
    "data" : tnpSample("data"   , eosSOSMuon2018 + "production_161122_muonSF_tnpTrees_data/SingleMuon_Run2018B_UL.root"     , lumi = 59.7 ),
}
