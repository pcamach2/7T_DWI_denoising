#!/bin/bash
#slurm_process_pipeline.sh

while getopts :p:s:z:m:f:l:b:t: option; do
	case ${option} in
    	p) export CLEANPROJECT=$OPTARG ;;
    	s) export CLEANSESSION=$OPTARG ;;
    	z) export CLEANSUBJECT=$OPTARG ;;
	m) export MINQC=$OPTARG ;;
	f) export fieldmaps=$OPTARG ;;
	l) export longitudinal=$OPTARG ;;
	b) export based=$OPTARG ;;
	t) export version=$OPTARG ;;
	esac
done
## takes project, subject, and session as inputs

IMAGEDIR=${based}/singularity_images
tmpdir=${based}/${version}/testing
scripts=${based}/${version}/scripts
stmpdir=${based}/${version}/scratch/stmp
scachedir=${based}/${version}/scratch/scache

## setup our variables and change to the session directory

echo ${CLEANPROJECT}
echo ${CLEANSUBJECT}
echo ${CLEANSESSION}
pwd

#translating naming conventions
echo "${CLEANSESSION: -1}"
session="${CLEANSESSION: -1}"
echo ${session}
project=${CLEANPROJECT}

subject="sub-"${CLEANSUBJECT}
sesname="ses-"${session}

scripts=${based}/${version}/scripts

IMAGEDIR=${based}/singularity_images

ses=${sesname:4}
sub=${subject:4}
projDir=${based}/${version}/testing/${project}
	
if [ -d "${projDir}/bids/sourcedata/${subject}/${sesname}/dwi" ];
then

module load singularity/3.8.5

scachedir=${based}/${version}/scratch/scache/${project}/${subject}/${sesname}
stmpdir=${based}/${version}/scratch/stmp/${project}/${subject}/${sesname}
mkdir -p ${based}/${version}/scratch/scache/${project}/${subject}/${sesname}
mkdir -p ${based}/${version}/scratch/stmp/${project}/${subject}/${sesname}

NOW=$(date +"%m-%d-%Y-%T")
echo "QSIprep started $NOW" >> ${scripts}/fulltimer.txt


# OMP_NTHREADS_VAL=$[SLURM_CPUS_PER_TASK-4]

SINGULARITY_CACHEDIR=${scachedir} SINGULARITY_TMPDIR=${stmpdir} singularity run --cleanenv --bind ${IMAGEDIR}:/imgdir,${stmpdir}:/sing_scratch,${projDir}:/data \
${IMAGEDIR}/qsiprep-v0.19.1.sif \
--fs-license-file /imgdir/license.txt /data/bids/sourcedata /data/bids/derivatives \
--output-resolution 1.6 --denoise-method dwidenoise --resource-monitor -w /sing_scratch \
--nthreads 24 --omp-nthreads 12 --mem_mb 40000 --longitudinal --separate-all-dwis \
--denoise-method none \
-vv --notrack --write-graph --pepolar-method TOPUP \
participant --participant-label ${subject}
 
#--bids-filter-file /data/bids/derivatives/qsiprep/config_${ses}.json

chmod 755 -R ${projDir}/bids/derivatives/qsiprep/${subject}/${sesname}
NOW=$(date +"%m-%d-%Y-%T")
echo "QSIprep finished $NOW" >> ${scripts}/fulltimer.txt

fi

