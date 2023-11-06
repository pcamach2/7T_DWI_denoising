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
tmpdir=${based}/${version}/dev
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
projDir=${based}/${version}/dev/${project}
	
if [ -d "${projDir}/bids/sourcedata/${subject}/${sesname}/dwi" ];
then

# module load singularity/3.8.5

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
--output-resolution 1.6 --resource-monitor -w /sing_scratch \
--nthreads 24 --omp-nthreads 12 --mem_mb 190000 --longitudinal --separate-all-dwis \
-vv --notrack --write-graph --recon_input /data/bids/derivatives/qsiprep \
--freesurfer-input /data/bids/derivatives/fmriprep/sourcedata/freesurfer \
--recon_spec dsi_studio_autotrack \
participant --participant-label ${subject}
 
chmod 777 -R ${projDir}/bids/derivatives/qsiprep/${subject}/${sesname}
NOW=$(date +"%m-%d-%Y-%T")
echo "QSIprep finished $NOW" >> ${scripts}/fulltimer.txt

#		NOW=$(date +"%m-%d-%Y-%T")
#		echo "QSIprep Recon started $NOW" >> ${scripts}/fulltimer.txt
#		SINGULARITY_CACHEDIR=${scachedir} SINGULARITY_TMPDIR=${stmpdir} singularity run --cleanenv --bind ${IMAGEDIR}:/imgdir,${stmpdir}:/sing_scratch,${projDir}:/data ${IMAGEDIR}/qsiprep-v0.17.0.sif --fs-license-file /imgdir/license.txt /data/bids/sourcedata /data/bids/derivatives --recon_input /data/bids/derivatives/qsiprep -freesurfer-input /data/bids/derivatives/fmriprep/sourcedata/freesurfer --recon_spec mrtrix_multishell_msmt_ACT-hsvs --output-resolution 1.6 -w /sing_scratch participant --participant-label ${subject}
#		SINGULARITY_CACHEDIR=${scachedir} SINGULARITY_TMPDIR=${stmpdir} singularity run --cleanenv --bind ${IMAGEDIR}:/imgdir,${stmpdir}:/sing_scratch,${projDir}:/data ${IMAGEDIR}/qsiprep-v0.17.0.sif --fs-license-file /imgdir/license.txt /data/bids/sourcedata /data/bids/derivatives --recon_input /data/bids/derivatives/qsiprep --recon_spec dsi_studio_gqi --output-resolution 1.6 -w /sing_scratch participant --participant-label ${subject}
#               SINGULARITY_CACHEDIR=${scachedir} SINGULARITY_TMPDIR=${stmpdir} singularity run --cleanenv --bind ${IMAGEDIR}:/imgdir,${stmpdir}:/sing_scratch,${projDir}:/data ${IMAGEDIR}/qsiprep-v0.17.0.sif --fs-license-file /imgdir/license.txt /data/bids/sourcedata /data/bids/derivatives --recon_input /data/bids/derivatives/qsiprep --recon_spec amico_noddi --output-resolution 1.6 -w /sing_scratch participant --participant-label ${subject}
#                NOW=$(date +"%m-%d-%Y-%T")
#		echo "QSIprep Recon finished $NOW" >> ${scripts}/fulltimer.txt
#		chmod 777 -R ${projDir}/bids/derivatives/qsirecon/${subject}*

#		SINGULARITY_CACHEDIR=${scachedir} SINGULARITY_TMPDIR=${stmpdir} singularity run --cleanenv --bind ${scripts}/matlab:/work,${scripts}/2019_03_03_BCT:/bctoolbox,${projDir}/bids/derivatives/qsirecon:/data ${IMAGEDIR}/matlab-R2019a.sif /work/qsinbs.sh "$subject" "$sesname"
#
#		SINGULARITY_CACHEDIR=${scachedir} SINGULARITY_TMPDIR=${stmpdir} singularity run --cleanenv --bind ${scripts}:/scripts,${projDir}/bids/derivatives/qsirecon/${subject}/${sesname}/dwi:/datain -W /datain ${IMAGEDIR}/pylearn.sif /scripts/gqimetrics.py
#		
#		SINGULARITY_CACHEDIR=${scachedir} SINGULARITY_TMPDIR=${stmpdir} singularity run --cleanenv --bind ${scripts}:/scripts,${projDir}/bids/derivatives/qsirecon/${subject}/${sesname}/dwi:/datanoddi ${IMAGEDIR}/neurodoc.sif /scripts/noddi_stats.sh "$subject" "$sesname"
		
fi

