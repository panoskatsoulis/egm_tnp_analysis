#!/bin/bash
#set -x

#INPUT=/eos/user/k/kpanos/www/SOS/LeptonSF_UL/Muons2018_pythoncondor
INPUT=/eos/user/k/kpanos/www/SOS/LeptonSF_UL/Muons2018_FullDYMC

#FIT_COMMAND="python tnpEGM_fitter.py settingsToRun.py --doFit --flag tightObject --doublePeak"
FIT_COMMAND="python tnpEGM_fitter.py etc/config/settings_SOS_Muon_2018_getBestFits.py --doFit --flag tightObject --doublePeak"

SETTINGS=etc/config/settings_SOS_Muon_2018_getBestFits.py

function applyCombToVoigtian() {
    mean1=$(echo $1 | awk -F'|' '{print $1}')
    widthP=$(echo $1 | awk -F'|' '{print $2}')
    sigma1=$(echo $1 | awk -F'|' '{print $3}')
    mean2=$(echo $1 | awk -F'|' '{print $4}')
    widthF=$(echo $1 | awk -F'|' '{print $5}')
    ratioP=$(echo $1 | awk -F'|' '{print $6}')
    ratioF=$(echo $1 | awk -F'|' '{print $7}')
    sed -i "s/_MEANV1P_/$mean1/" $SETTINGS
    sed -i "s/_MEANV1F_/$mean1/" $SETTINGS
    sed -i "s/_WIDTHP_/$widthP/" $SETTINGS
    sed -i "s/_SIGMAV1P_/$sigma1/" $SETTINGS
    sed -i "s/_SIGMAV1F_/$sigma1/" $SETTINGS
    sed -i "s/_MEANV2P_/$mean2/" $SETTINGS
    sed -i "s/_MEANV2F_/$mean2/" $SETTINGS
    sed -i "s/_WIDTHF_/$widthF/" $SETTINGS
    sed -i "s/_SIGMAVPRATIO_/$ratioP/" $SETTINGS
    sed -i "s/_SIGMAVFRATIO_/$ratioF/" $SETTINGS
    return
}

function applyCombToGaussian() {
    mean1=$(echo $1 | awk -F'|' '{print $1}')
    sigma1=$(echo $1 | awk -F'|' '{print $2}')
    mean2=$(echo $1 | awk -F'|' '{print $3}')
    sigma2=$(echo $1 | awk -F'|' '{print $4}')
    sed -i "s/_MEANG1P_/$mean1/" $SETTINGS
    sed -i "s/_MEANG1F_/$mean1/" $SETTINGS
    sed -i "s/_SIGMAG1P_/$sigma1/" $SETTINGS
    sed -i "s/_SIGMAG1F_/$sigma1/" $SETTINGS
    sed -i "s/_MEANG2P_/$mean2/" $SETTINGS
    sed -i "s/_MEANG2F_/$mean2/" $SETTINGS
    sed -i "s/_SIGMAG2P_/$sigma2/" $SETTINGS
    sed -i "s/_SIGMAG2F_/$sigma2/" $SETTINGS
    return
}


#for config in data_nominal data_altsig data_altbkg; do
for config in data_nominal; do
#for config in mc_nominal; do
    minDir=$INPUT/minFits_$config
    echo "====>" $minDir
    ls $minDir | grep ^bin | while read _BINTXT; do
	BIN=$(echo $_BINTXT | sed s/bin//)
	comb=$(head -n 1 `find $minDir/$_BINTXT | grep initialparams`)

	echo $minDir/$_BINTXT
	echo $comb

	cp etc/config/settings_template.py $SETTINGS
	sed -i "s@__INPUT__@\"$INPUT\"@" $SETTINGS
	sed -i "s@__OUTPUT__@\"$INPUT\"@" $SETTINGS

	echo Running $config $_BINTXT ...

	echo $minDir | grep data_nominal && {
	    applyCombToVoigtian $comb
	    eval "$FIT_COMMAND --iBin $BIN" &>nominal_data.log
	    grep "png has been created" nominal_data.log
	}

	echo $minDir | grep mc_nominal && {
	    applyCombToVoigtian $comb
	    eval "$FIT_COMMAND --mcSig --iBin $BIN" &>nominal_mc.log
	    grep "png has been created" nominal_mc.log
	}

	echo $minDir | grep altsig && {
	    applyCombToGaussian $comb
	    eval "$FIT_COMMAND --altSig --iBin $BIN" &>altsig_data.log
	    grep "png has been created" altsig_data.log
	}

	echo $minDir | grep altbkg && {
	    applyCombToVoigtian $comb
	    eval "$FIT_COMMAND --altBkg --iBin $BIN" &>altbkg_data.log
	    grep "png has been created" altbkg_data.log
	}

#	break
    done
done
