#!/usr/bin/env python3
import os, argparse, shutil
import subprocess as linux
from pprint import pprint
from numpy import arange, round, log10
from itertools import product

parser = argparse.ArgumentParser()

parser.add_argument("-input", default=None, help="Directory where the binning and the histograms exist")
parser.add_argument("-bin", required=True, help="The bin to refit recursively")
parser.add_argument("-fitsetup", default="nominal", help="This setup will be used to refit each bin (def: doublepeak nominal data fit)")
parser.add_argument("-count", default=False, action='store_true', help="Dont run the fits, just count the combinations for the initialisation of the params")
parser.add_argument("-test", default=False, action='store_true', help="Dont run ALL the fits, only the first 10")
parser.add_argument("-i","--interactive", default=False, action='store_true', help="Stop after every fit attempt to investigate")
args = parser.parse_args()

##### fit setup
if args.fitsetup == "nominal":
    setup = "--flag tightObject --doublePeak"
    name = "data_nominal"
elif args.fitsetup == "altsig":
    setup = "--flag tightObject --doublePeak --altSig"
    name = "data_altsig"
elif args.fitsetup == "altbkg":
    setup = "--flag tightObject --doublePeak --altBkg"
    name = "data_altbkg"
elif args.fitsetup == "mc":
    setup = "--flag tightObject --doublePeak --mcSig"
    name = "mc_nominal"
else:
    raise RuntimeError("Unknown fit setup:", args.fitsetup)

##### COMBS of params here
combs = {}
combs['mean1'] = ["90,85,95"]

dn, up, steps = 80, 140, 3
step = round((up-dn)/steps, 2)
combs['mean2'] = ["{},{},{}".format(val,
                                    round(val-step/2,2) if round(val-step/2,2)>dn else dn,
                                    round(val+step/2,2) if round(val+step/2,2)<up else up)
                  for val in round(arange(dn, up, step),2)]

dn, up, steps = 1, 7, 2
step = round((up-dn)/steps, 2)
combs['widthP'] = ["{},{},{}".format(val,
                                     round(val-step/2,2) if round(val-step/2,2)>dn else dn,
                                     round(val+step/2,2) if round(val+step/2,2)<up else up)
                   for val in round(arange(dn, up, step),2)]
#combs['widthP'] = ["2,0.9,5"]
#combs['widthF'] = ["2,0.9,5"]
combs['widthF'] = combs['widthP']

#combs['sigma1'] = ["2,0.5,5"]
dn, up, steps = 0.8, 5.0, 2
if args.fitsetup != "altsig":
    dn, up, steps = 0.8, 5.5, 2
step = round((up-dn)/steps, 2)
combs['sigma1'] = ["{},{},{}".format(val,
                                     round(val-step/2,2) if round(val-step/2,2)>dn else dn,
                                     round(val+step/2,2) if round(val+step/2,2)<up else up)
                   for val in round(arange(dn, up, step),2)]

# dn, up, steps = 0.5, 1, 1
# step = round((up-dn)/steps, 1)
# sigmaRatioP = ["{},{},{}".format(val,
#                                  round(val-step/2,2) if round(val-step/2,2)>dn else dn,
#                                  round(val+step/2,2) if round(val+step/2,2)<up else up)
#                for val in round(arange(dn, up, step),2)]
dn, up, steps = 7, 25, 3
step = round((up-dn)/steps, 1)
sigmaRatioP = ["{},{},{}".format(val,
                                 round(val-step/2,2) if round(val-step/2,2)>dn else dn,
                                 round(val+step/2,2) if round(val+step/2,2)<up else up)
               for val in round(arange(dn, up, step),2)]
combs['sigmaRatioP'] = sigmaRatioP
combs['sigmaRatioF'] = sigmaRatioP

## for gaussian 2
# dn, up, steps = 1, 70, 4
# step = round((up-dn)/steps, 2)
# combs['sigma2'] = ["{},{},{}".format(val,
#                                      round(val-step/2,2) if round(val-step/2,2)>dn else dn,
#                                      round(val+step/2,2) if round(val+step/2,2)<up else up)
#                    for val in round(arange(dn, up, step),2)]

pprint(combs)
if "altsig" in name:
    # signal Gaussian
    combs = product(combs['mean1'], combs['sigma1'], combs['mean2'], combs['sigma2'])
    combs = ["{}|{}|{}|{}".format(m1,s1,m2,s2) for m1,s1,m2,s2 in combs]
else:
    # signal Voigtian
    combs = product(combs['mean1'], combs['widthP'], combs['sigma1'],
                    combs['mean2'], combs['widthF'], combs['sigmaRatioP'], combs['sigmaRatioF'])
    combs = ["{}|{}|{}|{}|{}|{}|{}".format(m1,wP,s1,m2,wF,sRP,sRF) for m1,wP,s1,m2,wF,sRP,sRF in combs]
    # combs = product(combs['mean1'], combs['width'],
    #                 combs['sigma1'], combs['mean2'], combs['sigmaRatioP'])
    # combs = ["{}|{}|{}|{}|{}|{}".format(m1,w,s1,m2,sRP,sRP) for m1,w,s1,m2,sRP in combs]
print("Combinations counted", len(combs))
pprint(combs)
if args.count: quit(0)
##### COMBS of params here




##### Prepare directories & environment
_bin="bin"+args.bin
bestfit = "{}/minFits_{}".format(args.input, name)
if not os.path.exists(bestfit+"/allbins"):
    os.makedirs(bestfit+"/allbins")
tmpfit = "{}/tmpBestFits/{}/{}".format(args.input,name,_bin)
if os.path.exists(tmpfit):
    print(">> Removing old tmp fits ({}) ...".format(tmpfit))
    shutil.rmtree(tmpfit, ignore_errors=True) #clean old tmp
os.makedirs(tmpfit)

os.chdir("/afs/cern.ch/user/k/kpanos/work/Projects/Displaced_Charginos/sos_framework_latest/displaced/tmp/CMSSW_10_6_26/src/CMGTools/egm_tnp_analysis")
linux.run('eval `scramv1 runtime -sh`', shell=True)
print(">> in dir", os.getcwd())

##### Init best values
minFCN_p, minFCN_f = 99999, 99999
minEDM_p, minEDM_f = 99999, 99999
targEDM = float("1e-6")

def applyCombToVoigtian(_comb, _file):
    mean1, widthP, sigma1, mean2, widthF, sigmaRP, sigmaRF = _comb.split('|')
    linux.run("sed -i s/_MEANV1P_/{}/ {}.py".format(mean1, _file)           , shell=True)
    linux.run("sed -i s/_MEANV1F_/{}/ {}.py".format(mean1, _file)           , shell=True)
    linux.run("sed -i s/_WIDTHP_/{}/ {}.py".format(widthP, _file)           , shell=True)
    linux.run("sed -i s/_SIGMAV1P_/{}/ {}.py".format(sigma1, _file)         , shell=True)
    linux.run("sed -i s/_SIGMAV1F_/{}/ {}.py".format(sigma1, _file)         , shell=True)
    linux.run("sed -i s/_MEANV2P_/{}/ {}.py".format(mean2, _file)           , shell=True)
    linux.run("sed -i s/_MEANV2F_/{}/ {}.py".format(mean2, _file)           , shell=True)
    linux.run("sed -i s/_WIDTHF_/{}/ {}.py".format(widthF, _file)           , shell=True)
    linux.run("sed -i s/_SIGMAVPRATIO_/{}/ {}.py".format(sigmaRP, _file)    , shell=True)
    linux.run("sed -i s/_SIGMAVFRATIO_/{}/ {}.py".format(sigmaRF, _file)    , shell=True)

def applyCombToGaussian(_comb, _file):
    mean1, sigma1, mean2, sigma2 = _comb.split('|')
    linux.run("sed -i s/_MEANG1P_/{}/ {}.py".format(mean1, _file)           , shell=True)
    linux.run("sed -i s/_MEANG1F_/{}/ {}.py".format(mean1, _file)           , shell=True)
    linux.run("sed -i s/_SIGMAG1P_/{}/ {}.py".format(sigma1, _file)         , shell=True)
    linux.run("sed -i s/_SIGMAG1F_/{}/ {}.py".format(sigma1, _file)         , shell=True)
    linux.run("sed -i s/_MEANG2P_/{}/ {}.py".format(mean2, _file)           , shell=True)
    linux.run("sed -i s/_MEANG2F_/{}/ {}.py".format(mean2, _file)           , shell=True)
    linux.run("sed -i s/_SIGMAG2P_/{}/ {}.py".format(sigma2, _file)         , shell=True)
    linux.run("sed -i s/_SIGMAG2F_/{}/ {}.py".format(sigma2, _file)         , shell=True)


def keepThisFit(_comb, tmpreport):
    bestfit_forbin = bestfit+'/'+_bin
    if os.path.exists(bestfit_forbin): shutil.rmtree(bestfit_forbin, ignore_errors=True)
    report = os.open("{}/bestfit_report.log".format(tmpfit, _bin), os.O_RDWR | os.O_CREAT)
    os.write(report, linux.check_output("cat {}".format(tmpreport), shell=True)) #this returns directly 'bytes' object
    os.close(report)
    initparams = os.open("{}/initialparams.log".format(tmpfit, _bin), os.O_RDWR | os.O_CREAT)
    os.write(initparams, (_comb+'\n').encode())
    os.close(initparams)
    linux.run("cp -r {} {}/".format(tmpfit, bestfit), shell=True)
    linux.run('cp $(ls {a}/plots/*/*/*png) {b}/allbins/$(ls {a}/plots/*/*/*png | sed "s/[)(]//g; s@.*/@@")'.format(
        a=bestfit_forbin, b=bestfit),
              shell=True
    )

def getFCNEDMfromReport(_report):
    res = {}
    ## extract FCNs and EDMs (find first the line where "STATUS=CONVERGED" and get the appropriate EDM)
    FCNtext_p = str(linux.getoutput("cat {} | grep 'PASSED PROBES' -A 1 | grep -v '====' | awk -F'[ =]' '{{print $6}}'".format(_report)))
    res['FCN_p'] = float(FCNtext_p)
    res['fitConverged_p'] = bool(linux.check_output("cat {} | grep fcn={}.*status=converged -i | awk '{{print $1\" \"$4}}' | sort -u".format(_report, FCNtext_p), shell=True))
    res['EDM_p'] = 99999
    if res['fitConverged_p']:
        values = linux.getoutput("cat {} | grep fcn={}.*status=converged -i -A 1 | grep EDM | sed s/STRATEGY.*// | awk -F'=' '{{print $2}}'".format(_report, FCNtext_p)).split("\n")
        for val in values:
            res['EDM_p'] = float(val) if float(val)<res['EDM_p'] else res['EDM_p']
    #
    FCNtext_f = str(linux.getoutput("cat {} | grep 'FAILED PROBES' -A 1 | grep -v '====' | awk -F'[ =]' '{{print $6}}'".format(_report)))
    res['FCN_f'] = float(FCNtext_f)
    res['fitConverged_f'] = bool(linux.check_output("cat {} | grep fcn={}.*status=converged -i | awk '{{print $1\" \"$4}}' | sort -u".format(_report, FCNtext_f), shell=True))
    res['EDM_f'] = 99999
    if res['fitConverged_f']:
        values = linux.getoutput("cat {} | grep fcn={}.*status=converged -i -A 1 | grep EDM | sed s/STRATEGY.*// | awk -F'=' '{{print $2}}'".format(_report, FCNtext_f)).split("\n")
        for val in values:
            res['EDM_f'] = float(val) if float(val)<res['EDM_f'] else res['EDM_f']
    return res

def getOldBestFit():
    return getFCNEDMfromReport(bestfit+'/'+_bin+"/bestfit_report.log")

import readline
def interactiveMode(res):
    _help = '''
    h/help : print help
    c/n    : continue to the next fit
    unt    : run until a better fit is found
    q      : quit
    old    : load an old "bestfit" stored in "minFits_*_*/bin_*" dir
    mins   : print minimums and the best fit
    k      : keep this fit
    d      : drop this fit
    ch     : change which fit is considered 'best'
    '''
    while True:
        cmd = input('intr mode > ')
        if cmd in ["h", "help"]:
            print(_help)
            continue
        if cmd == "q":
            quit(0)
        if cmd in ["c", "n"]:
            return
        if cmd == "unt":
            res['until'] = True
            return
        if cmd == "mins":
            print("minFCN_p", minFCN_p)
            print("minFCN_f", minFCN_f)
            print("minEDM_p", minEDM_p)
            print("minEDM_f", minEDM_f)
            print("best fit:", "passing" if minEDM_p < minEDM_f else "failing")
            continue
        if cmd == "k":
            res['keepthis'] = True
            return
        if cmd == "d":
            res['dropthis'] = True
            return
        if cmd == "ch":
            if minEDM_p < minEDM_f:
                res['best_p'] = False
                res['best_f'] = True
            else:
                res['best_p'] = True
                res['best_f'] = False
            continue
        if cmd == "old":
            values = getOldBestFit()
            minFCN_p = values['FCN_p']
            minFCN_f = values['FCN_f']
            minEDM_p = values['EDM_p']
            minEDM_f = values['EDM_f']
            continue
        if cmd != "":
            print("Unknown command", cmd)
            print(_help)

def resetIntrOptions(opt):
    for name in opt.keys():
        opt[name] = False

intr_res = {'keepthis' : False,
            'dropthis' : False,
            'best_p'   : False,
            'best_f'   : False,
            'until'    : False}
for i,comb in enumerate(combs):
    settings = "settings_to_run_{}_{}".format(name,_bin)
    linux.run("cp etc/config/settings_SOS_Muon_2018_template.py {}.py".format(settings), shell=True)
    ##
    ## modify new settings
    linux.run('sed -i s@__INPUT__@\\"{}\\"@ {}.py'.format(args.input, settings)  , shell=True)
    linux.run('sed -i s@__OUTPUT__@\\"{}\\"@ {}.py'.format(tmpfit, settings)     , shell=True)
    if "altSig" in setup:
        applyCombToGaussian(comb, settings)
    else:
        applyCombToVoigtian(comb, settings)
    ##
    ## run the fit
    report = "report_last_fit_{}_{}".format(name,_bin)
    fitcommand = "python tnpEGM_fitter.py {}.py --doFit {} --iBin {} &>{}".format(settings, setup, args.bin, report)
    print(">>", fitcommand)
    linux.run(fitcommand, shell=True)
    linux.run("echo Progress: {:.2f}% >> {}".format(100*(i+1)/len(combs), report), shell=True) # write the progress in all tmp fits
    ##
    ## extract FCNs and EDMs (find first the line where "STATUS=CONVERGED" and get the appropriate EDM)
    values = getFCNEDMfromReport(report)
    FCN_p, FCN_f = values['FCN_p'], values['FCN_f']
    EDM_p, EDM_f = values['EDM_p'], values['EDM_f']
    fitConverged_p = values['fitConverged_p']
    fitConverged_f = values['fitConverged_f']
    # FCNtext_p = str(linux.getoutput("cat {} | grep 'PASSED PROBES' -A 1 | grep -v '====' | awk -F'[ =]' '{{print $6}}'".format(report)))
    # FCN_p = float(FCNtext_p)
    # fitConverged_p = bool(linux.check_output("cat {} | grep fcn={}.*status=converged -i | awk '{{print $1\" \"$4}}' | sort -u".format(report, FCNtext_p), shell=True))
    # EDM_p = 99999
    # if fitConverged_p:
    #     values = linux.getoutput("cat {} | grep fcn={}.*status=converged -i -A 1 | grep EDM | sed s/STRATEGY.*// | awk -F'=' '{{print $2}}'".format(report, FCNtext_p)).split("\n")
    #     for val in values:
    #         EDM_p = float(val) if float(val)<EDM_p else EDM_p
    # #
    # FCNtext_f = str(linux.getoutput("cat {} | grep 'FAILED PROBES' -A 1 | grep -v '====' | awk -F'[ =]' '{{print $6}}'".format(report)))
    # FCN_f = float(FCNtext_f)
    # fitConverged_f = bool(linux.check_output("cat {} | grep fcn={}.*status=converged -i | awk '{{print $1\" \"$4}}' | sort -u".format(report, FCNtext_f), shell=True))
    # EDM_f = 99999
    # if fitConverged_f:
    #     values = linux.getoutput("cat {} | grep fcn={}.*status=converged -i -A 1 | grep EDM | sed s/STRATEGY.*// | awk -F'=' '{{print $2}}'".format(report, FCNtext_f)).split("\n")
    #     for val in values:
    #         EDM_f = float(val) if float(val)<EDM_f else EDM_f
    #
    varsAtLimit = bool(linux.getoutput("cat {} | grep WARNING -A 1 | grep 'AT ITS .* ALLOWED LIMIT'".format(report)))
    fitsAreAccepted = fitConverged_p and fitConverged_f
    ##
    ## identify if these 2 fits are better than the best
    if intr_res['best_p']:
        # forced best fitted, pass fit is better fitted
        betterfit_goesBetter = (FCN_p<minFCN_p or (EDM_p<minEDM_p and FCN_p==minFCN_p))
        worsefit_goesBetter = (FCN_f<minFCN_f or (EDM_f<minEDM_f and FCN_f==minFCN_f))
        betterfit_FCNmove = abs((FCN_p-minFCN_p)/minFCN_p)
        betterfit_edm = EDM_p
    elif intr_res['best_f']:
        # forced best fitted, fail fit is better fitted
        betterfit_goesBetter = (FCN_f<minFCN_f or (EDM_f<minEDM_f and FCN_f==minFCN_f))
        worsefit_goesBetter = (FCN_p<minFCN_p or (EDM_p<minEDM_p and FCN_p==minFCN_p))
        betterfit_FCNmove = abs((FCN_f-minFCN_f)/minFCN_f)
        betterfit_edm = EDM_f
    elif minEDM_p < minEDM_f:
        # up to now, pass fit is better fitted
        betterfit_goesBetter = (FCN_p<minFCN_p or (EDM_p<minEDM_p and FCN_p==minFCN_p))
        worsefit_goesBetter = (FCN_f<minFCN_f or (EDM_f<minEDM_f and FCN_f==minFCN_f))
        betterfit_FCNmove = abs((FCN_p-minFCN_p)/minFCN_p)
        betterfit_edm = EDM_p
    else:
        # up to now, fail fit is better fitted
        betterfit_goesBetter = (FCN_f<minFCN_f or (EDM_f<minEDM_f and FCN_f==minFCN_f))
        worsefit_goesBetter = (FCN_p<minFCN_p or (EDM_p<minEDM_p and FCN_p==minFCN_p))
        betterfit_FCNmove = abs((FCN_f-minFCN_f)/minFCN_f)
        betterfit_edm = EDM_f
    ##
    ## Decision
    decision = ( (fitsAreAccepted and minFCN_p>0 and minFCN_f>0)
                 or (fitsAreAccepted and betterfit_goesBetter and worsefit_goesBetter)
                 or (fitsAreAccepted and not betterfit_goesBetter and betterfit_FCNmove<0.01 and worsefit_goesBetter) )
    ##
    ## interactive mode
    if args.interactive:
        if intr_res['until'] and not decision: continue
        print("Combination:", comb)
        print("Passing: FCN={} | EDM={} | converged={}".format(FCN_p, EDM_p, fitConverged_p))
        print("Failing: FCN={} | EDM={} | converged={}".format(FCN_f, EDM_f, fitConverged_f))
        print("Any Variables AT LIMIT", varsAtLimit)
        print("Better goesBetter", betterfit_goesBetter)
        print("Worse goesBetter", worsefit_goesBetter)
        print("Decision:", decision)
        resetIntrOptions(intr_res)
        interactiveMode(intr_res)
    ## will keep the new fits in case both are better or
    ## the worst is better and the best is worse by ~half order of magn.
    ## the worst is better and the best got worse but still under EDM target
    if (intr_res['keepthis'] or decision) and not intr_res['dropthis']:
        print(">> will store the fit {} ...".format(comb))
        keepThisFit(comb, report)
        minFCN_p, minFCN_f = FCN_p, FCN_f
        minEDM_p, minEDM_f = EDM_p, EDM_f
    ##
    ## break if this is a test
    if args.test and i==49:
        break

quit(0)
#### EXAMPLES
## get list of files in dir
#files = filter(lambda f: f.is_dir(), os.scandir(args._input))
## run linux command and get output
#_yield = int(linux.check_output("cat {}/yields.txt | grep -i data | grep -o \"[0-9]*\"".format(_f.path), shell=True))
