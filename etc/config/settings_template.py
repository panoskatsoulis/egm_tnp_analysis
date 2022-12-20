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

inDir = __INPUT__
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

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,"nP[3,-5,5]","sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]","nF[3,-5,5]","sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
]

tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
]


tnpParDoublePeakNomFit = [
#    "meanP1[90,80,100]", "widthP[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,2.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
#    "meanF1[90,80,100]", "widthF[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    "meanP1[_MEANV1P_]","widthP[_WIDTHP_]","sigmaP1[_SIGMAV1P_]","meanP2[_MEANV2P_]","sigmaPRatio[_SIGMAVPRATIO_]",
    "meanF1[_MEANV1F_]","widthF[_WIDTHF_]","sigmaF1[_SIGMAV1F_]","meanF2[_MEANV2F_]","sigmaFRatio[_SIGMAVFRATIO_]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
]

tnpParDoublePeakAltSigFit = [
#    "meanP1[90,80,100]","sigmaP1[0.9,0.5,5.0]","meanP2[90,20,110]","sigmaP2[0.9,0.5,5.0]",
#    "meanF1[90,80,100]","sigmaF1[0.9,0.5,5.0]","meanF2[90,20,110]","sigmaF2[0.9,0.5,5.0]",
    "meanP1[_MEANG1P_]","sigmaP1[_SIGMAG1P_]","meanP2[_MEANG2P_]","sigmaP2[_SIGMAG2P_]",
    "meanF1[_MEANG1F_]","sigmaF1[_SIGMAG1F_]","meanF2[_MEANG2F_]","sigmaF2[_SIGMAG2F_]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
]
     
tnpParDoublePeakAltBkgFit = [
#    "meanP1[90,80,100]", "widthP[2.5,2.0,3.0]", "sigmaP1[1.0,0.5,2.5]", "meanP2[90,20,100]", "sigmaPRatio[4,1.5,10]",
#    "meanF1[90,80,100]", "widthF[2.5,2.0,3.0]", "sigmaF1[1.0,0.5,2.5]", "meanF2[90,20,100]", "sigmaFRatio[4,1.5,10]",
    "meanP1[_MEANV1P_]","widthP[_WIDTHP_]","sigmaP1[_SIGMAV1P_]","meanP2[_MEANV2P_]","sigmaPRatio[_SIGMAVPRATIO_]",
    "meanF1[_MEANV1F_]","widthF[_WIDTHF_]","sigmaF1[_SIGMAV1F_]","meanF2[_MEANV2F_]","sigmaFRatio[_SIGMAVFRATIO_]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
]
