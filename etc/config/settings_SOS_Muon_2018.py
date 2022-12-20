#############################################################
########## General settings
#############################################################
Probe_isTightNoIso = "Probe_isClean && abs(Probe_ip3d)<0.01 && Probe_sip3d<2"
flags = {
    "looseObject"    : "Probe_isClean",
    "tightNoIsoObject"    : Probe_isTightNoIso,
    "tightObjectOverTightNoIso"    : "Probe_isTight",
    "tightObject"    : "Probe_isTight",
}

inDir = "/eos/user/k/kpanos/www/SOS/LeptonSF_UL/Muons2018_FullDYMC"
baseOutDir = inDir

#############################################################
########## samples definition  - preparing the samples
#############################################################
import etc.inputs.tnpSampleDef_SOS_Muon_2018 as tnpSamples
tnpTreeDir = "./Events"

samplesDef = {
    "data"   : tnpSamples.SOS_Muon_2018["data"].clone(),
    "mcNom"  : tnpSamples.SOS_Muon_2018["DY"].clone(),
    "mcAlt"  : tnpSamples.SOS_Muon_2018["DY"].clone(),
    "tagSel" : tnpSamples.SOS_Muon_2018["DY"].clone(),
}

# Set tree name/directory
samplesDef["data" ].set_tnpTree(tnpTreeDir)
if not samplesDef["mcNom" ] is None: samplesDef["mcNom" ].set_tnpTree(tnpTreeDir)
if not samplesDef["mcAlt" ] is None: samplesDef["mcAlt" ].set_tnpTree(tnpTreeDir)
if not samplesDef["tagSel"] is None: samplesDef["tagSel"].set_tnpTree(tnpTreeDir)

# Set MC truth
if not samplesDef["mcNom" ] is None: samplesDef["mcNom" ].set_mcTruth()
if not samplesDef["mcAlt" ] is None: samplesDef["mcAlt" ].set_mcTruth()
if not samplesDef["tagSel"] is None: samplesDef["tagSel"].set_mcTruth()

# Set PU weight
#weightName = "puWeight"
weightName = "1.0"
if not samplesDef["mcNom" ] is None: samplesDef["mcNom" ].set_weight(weightName)
if not samplesDef["mcAlt" ] is None: samplesDef["mcAlt" ].set_weight(weightName)
if not samplesDef["tagSel"] is None: samplesDef["tagSel"].set_weight(weightName)


#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
    { 'var' : 'abs(Probe_eta)' , 'type': 'float', 'bins': [0.0, 1.2, 2.4] },
    { 'var' : 'Probe_pt' , 'type': 'float', 'bins': [3.5, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 1000.0] },
]


#############################################################
########## Cuts definition for all samples
#############################################################
cutBase   = "Tag_pt > 29 && abs(Tag_eta) < 2.4 && Tag_tightId && Tag_isGenMatched && Probe_pt > 3.5 && abs(Probe_eta) < 2.4 && Probe_looseId && Probe_isGenMatched && TnP_trigger && Probe_charge*Tag_charge < 0" # tightNoIsoObject
#cutBase   = "Tag_pt > 29 && abs(Tag_eta) < 2.4  && Tag_tightId && Tag_isGenMatched && Probe_pt > 3.5 && abs(Probe_eta) < 2.4 && Probe_looseId && Probe_isGenMatched && TnP_trigger && Probe_charge*Tag_charge < 0 && " + Probe_isTightNoIso # tightObjectOverTightNoIso

additionalCuts = {}


#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
]

tnpParDoublePeakNomFit = [
    "meanP1[90,80,100]", "widthP[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,2.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    "meanF1[90,80,100]", "widthF[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",

    ##################### MC #####################
    # bin00
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.0,0.5,1.8]", "meanP2[65,60,70]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,2.0]", "meanF2[90,20,100]", "sigmaFRatio[8,7.5,10]",
    # bin05
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.0,0.5,1.8]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,1.6]", "meanF2[45,40,50]", "sigmaFRatio[8,6.5,10]",
    # bin12
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[0.9,0.5,1.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,1.1]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin13
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.0,0.5,1.6]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,1.9]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin14
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[0.9,0.5,1.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin15
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.0,0.5,1.6]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,1.9]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin16
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[0.9,0.5,1.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,1.1]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin17
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.4]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin18
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.1]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin19
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.7]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",

    ##################### DATA #####################
    # bin00
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.8]", "meanP2[69]", "sigmaPRatio[7.6]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[2.0]", "meanF2[90,85,95]", "sigmaFRatio[5,1.0,20.0]",
    # bin01
    #"meanP1[90,88,98]", "width[2.2]", "sigmaP1[1.6]", "meanP2[73]", "sigmaPRatio[7.5]",
    #"meanF1[90,88,98]", "width[2.2]", "sigmaF1[1.6]", "meanF2[66]", "sigmaFRatio[8.8]",
    # bin02
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.7]", "meanP2[68]", "sigmaPRatio[7.7]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.8]", "meanF2[90,88,92]", "sigmaFRatio[5,1.0,20.0]",
    # bin03
    #"meanP1[90,88,92]", "width[3.0]", "sigmaP1[1.3]", "meanP2[71]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,95]", "width[3.0]", "sigmaF1[1.5]", "meanF2[90,88,92]", "sigmaFRatio[2.5]",
    # bin04
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.6]", "meanP2[68]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.3]", "meanF2[90,88,92]", "sigmaFRatio[4,1.5,10]",
    # bin05
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.6]", "meanP2[71]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.6]", "meanF2[90,88,92]", "sigmaFRatio[4,1.5,10]",
    # bin06
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.5]", "meanP2[74]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.4]", "meanF2[90,88,92]", "sigmaFRatio[4,1.5,10]",
    # bin07
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.5]", "meanP2[74]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.7]", "meanF2[90,88,92]", "sigmaFRatio[4,1.5,10]",
    # bin09
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin10
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[0.7,0.5,0.9]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin11
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.4]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin12
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[0.9,0.5,1.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin13
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.8]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin14
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.0,0.5,2.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin18
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.1]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",


    ####################### MC #####################
    # bin00
    #"meanP1[90,80,100]", "width[2.5,1.5,3.0]", "sigmaP1[1.0,0.5,1.5]", "meanP2[90,60,65]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,1.5,3.0]", "sigmaF1[1.0,0.5,1.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin01
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,1.2]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,1.2]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin02
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.6,0.5,1.7]", "meanP2[90,68,72]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.5,1.0,1.6]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin04
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,1.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[2,0.5,3]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin05
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,1.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.0]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin06
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,2.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.0]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin12
    #"meanP1[90,80,100]", "width[1.5,1.0,2.0]", "sigmaP1[0.7,0.5,1.1]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[1.5,1.0,2.0]", "sigmaF1[0.7,0.5,1.2]", "meanF2[94,90,93]", "sigmaFRatio[4,1.5,10]",
    # bin13
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.7,0.5,1.1]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,1.3]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin14
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.4,0.3,0.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,1.1]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin15
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.7,0.3,1.1]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,1.3]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin16
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.5,0.3,0.7]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[0.6,0.5,0.9]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin17
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.5,0.3,1.3]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[0.6,0.5,1.15]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin18
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.5,0.3,0.9]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[0.6,0.5,1.15]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin19
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.5,0.3,1.4]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[0.6,0.5,2.0]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",

    ####################### DATA #####################
    # bin00
    #"meanP1[90,80,100]", "width[2.5,1.5,3.0]", "sigmaP1[1.0,0.5,1.5]", "meanP2[90,60,65]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,1.5,3.0]", "sigmaF1[1.0,0.5,1.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin02, bin03, bin04
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.3,0.6]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin05
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.7,0.5,1.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin06
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.7,0.3,0.8]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[2.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin07
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[0.2,0.1,0.4]", "meanP2[80,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,1.4]", "meanF2[90,60,100]", "sigmaFRatio[3,2.0,5.0]",
    #"acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    #"acmsF[60.,50.,75.]","betaF[0.01]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    # bin09
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,1.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin13
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,1.75]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin15
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,1.8]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90]", "sigmaFRatio[4,1.5,10]",
    # bin17
    #"meanP1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,2.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90]", "sigmaFRatio[4,1.5,10]",
    # bin19
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.4]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[2.5,2.0,3.5]", "meanF2[90]", "sigmaFRatio[6,5.0,10]",
]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",

    ##################### MC #####################
    # bin11
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[1.5]","sosF[1,0.5,5.0]",
    # bin12
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[1.1]","sosF[1,0.5,5.0]",
    # bin13
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,1.7]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,1.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[2.0,0.5,2.0]","sosF[1,0.5,5.0]",
    # bin14
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[2.0,0.5,1.5]","sosF[1,0.5,5.0]",
    # bin15
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,1.5]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[1.5,0.5,1.8]","sosF[1,0.5,5.0]",
    # bin17
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,1.7]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[2.0,0.5,2.3]","sosF[1,0.5,5.0]",
    # bin19
    #"meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,1.9]","sosP[1,0.5,5.0]",
    #"meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
]

tnpParDoublePeakAltSigFit = [
    "meanP1[90,80,100]","sigmaP1[0.9,0.5,5.0]","meanP2[90,20,110]","sigmaP2[0.9,0.5,5.0]",
    "meanF1[90,80,100]","sigmaF1[0.9,0.5,5.0]","meanF2[90,20,110]","sigmaF2[0.9,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
]
     
tnpParDoublePeakAltBkgFit = [
    "meanP1[90,80,100]", "widthP[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,2.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    "meanF1[90,80,100]", "widthF[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",

    # bin00
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.8]", "meanP2[69]", "sigmaPRatio[7.6]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[2.0]", "meanF2[90,85,95]", "sigmaFRatio[5,1.0,20.0]",
    # bin01
    #"meanP1[90,88,98]", "width[2.2]", "sigmaP1[1.6]", "meanP2[73]", "sigmaPRatio[7.5]",
    #"meanF1[90,88,98]", "width[2.2]", "sigmaF1[1.6]", "meanF2[90,88,92]", "sigmaFRatio[5,1.0,20.0]",
    #"alphaF[-0.032]",
    # bin02
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.8]", "meanF2[90,88,92]", "sigmaFRatio[5,1.0,20.0]",
    # bin03
    #"meanP1[90,88,92]", "width[3.0]", "sigmaP1[1.3]", "meanP2[71]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,95]", "width[3.0]", "sigmaF1[1.5]", "meanF2[90,88,92]", "sigmaFRatio[2.5]",
    # bin04
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.6]", "meanP2[68]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.3]", "meanF2[90,88,92]", "sigmaFRatio[4,1.5,10]",
    # bin05
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.6]", "meanP2[71]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.6]", "meanF2[90,88,92]", "sigmaFRatio[4,1.5,10]",
    # bin06
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.5]", "meanP2[74]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.4]", "meanF2[70,60,80]", "sigmaFRatio[4,1.5,10]",
    # bin07
    #"meanP1[90,88,92]", "width[2.0]", "sigmaP1[1.5]", "meanP2[74]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,88,92]", "width[2.0]", "sigmaF1[1.7]", "meanF2[70,60,80]", "sigmaFRatio[4,1.5,10]",
    # bin08
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[0.9]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin09
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin10
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[0.7,0.5,0.9]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin11
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.4]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin12
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[0.9,0.5,1.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin13
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0,0.5,1.8]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin14
    #"meanP1[90,80,100]", "width[2.0]", "sigmaP1[1.0,0.5,2.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[2.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin16
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.0]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    # bin19
    #"meanP1[90,80,100]", "width[3.0]", "sigmaP1[1.7]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
    #"meanF1[90,80,100]", "width[3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
]
