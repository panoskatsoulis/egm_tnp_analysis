from ROOT import gROOT, TCanvas
gROOT.LoadMacro('./libCpp/RooCBExGaussShape.cc')
gROOT.LoadMacro('./libCpp/RooCMSShape.cc')
from ROOT import RooArgList, RooRealVar, RooCMSShape, RooCBExGaussShape, RooVoigtian, RooAddPdf, RooRealSumPdf, RooRealConstant, RooGaussian

## useful functions
'''
        "Gaussian::sigResPass(x,meanP,sigmaP)",
        "Gaussian::sigResFail(x,meanF,sigmaF)",
        "RooCMSShape::bkgPass(x, acmsP, betaP, gammaP, peakP)",
        "RooCMSShape::bkgFail(x, acmsF, betaF, gammaF, peakF)",


        "RooCBExGaussShape::sigResPass(x,meanP,expr('sqrt(sigmaP*sigmaP+sosP*sosP)',{sigmaP,sosP}),alphaP,nP, expr('sqrt(sigmaP_2*sigmaP_2+sosP*sosP)',{sigmaP_2,sosP}),tailLeft)",
        "RooCBExGaussShape::sigResFail(x,meanF,expr('sqrt(sigmaF*sigmaF+sosF*sosF)',{sigmaF,sosF}),alphaF,nF, expr('sqrt(sigmaF_2*sigmaF_2+sosF*sosF)',{sigmaF_2,sosF}),tailLeft)",


        "Exponential::bkgPass(x, alphaP)",
        "Exponential::bkgFail(x, alphaF)",


        "Voigtian::sigResPass1(x, meanP1, width, sigmaP1)",
        "Voigtian::sigResPass2(x, meanP2, width, prod::sigmaP2(sigmaP1, sigmaPRatio))",
        "Voigtian::sigResFail1(x, meanF1, width, sigmaF1)",
        "Voigtian::sigResFail2(x, meanF2, width, prod::sigmaF2(sigmaF1, sigmaFRatio))",

'''

## required variables
x = RooRealVar("x","mass",0,160)
alpha = RooRealVar("alpha","alpha", 60) #[50-75]
beta = RooRealVar("beta","beta", 0.04) #[0.01-0.06]
gamma = RooRealVar("gamma","gamma", 0.1) #[0.005-1]
peak = RooRealVar("peak","peak",90.)
mean = RooRealVar("mean","mean", 90) #[80-100]
width = RooRealVar("width","width", 2) #[C]
sigma = RooRealVar("sigma","sigma", 0.7) #[0.5-1]
## shape to plot on canvas
shape_bkg = RooCMSShape("bkg", "CMS Shape",
                        x, alpha, beta, gamma, peak)
shape_sig = RooVoigtian("sig", "Voigtian",
                        x, mean, width, sigma)
shape_gaus = RooGaussian("sig", "Gaussian",
                        x, mean, sigma)
#shape = RooRealSumPdf("shape","s+b",RooArgList(shape_sig,shape_bkg),RooArgList(RooRealVar('c1','c1',1),RooRealVar('c2','c2',1)));
#shape = shape_gaus
shape = shape_sig
#shape = shape_bkg

## plotting
def plot(_shape):
    plot = x.frame()
    _shape.plotOn(plot)
    canv = TCanvas("canv", "canv", 600, 600)
    canv.cd()
    plot.Draw()
    canv.Draw()
    return
plot(shape)

import readline
while True:
    toexec = raw_input('what next? [q/r]')

    if toexec == 'q':
        print "Quitting ..."
        quit(0)

    if toexec == 'r':
        print "Replotting ... [type 'quit' to stop]"
        while True:
            shape.Print()
            print ["{}: {}".format(var.GetName(),var.getVal()) for var in shape.getVariables()]
            values = raw_input("Set Values for the vars above > ").split(',')
            if values[0] == 'quit': quit(0)
            print values
            for var, val in zip(shape.getVariables(), values):
                var.setVal(float(val))
            plot(shape)
