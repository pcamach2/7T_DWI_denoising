#!/bin/bash
#
#SBATCH --job-name=CUPS_denoising_test
#SBATCH --output=CUPS_denoising_test.txt
#SBATCH --ntasks-per-node=1
#SBATCH --time=14:00:00

proj=$1
base_dir=$2
version=$3
scripts=${base_dir}/${version}/scripts
projDir=${base_dir}/${version}/testing/${proj}

NOW=$(date "+%D-%T")
if [ ${#SLURM_ARRAY_TASK_ID} == 1 ];
then
        inputNo="00${SLURM_ARRAY_TASK_ID}"
	subject="sub-${proj}${inputNo}"
	echo "$1 started $NOW" > ${scripts}/dyno_$1_test_${inputNo}.txt

singularity run --cleanenv -B ${projDir}:/datain,${projDir}/denoising_test:/timer \
-B ${scripts}/denoising_comp.py:/scripts/denoising_comp.py \
${base_dir}/singularity_images/dipy_testbed.sif \
/datain/bids/derivatives/dipy_denoising/${subject} ${subject}

	NOW=$(date "+%D-%T")
	echo "$1 finished $NOW" >> ${scripts}/dyno_$1_test_${inputNo}.txt
	exit 0
elif [ ${#SLURM_ARRAY_TASK_ID} == 2 ];
then
        inputNo="0${SLURM_ARRAY_TASK_ID}"
	subject="sub-${proj}${inputNo}"
        echo "$1 started $NOW" > ${scripts}/dyno_$1_test_${inputNo}.txt
	
singularity run --cleanenv -B ${projDir}:/datain,${projDir}/denoising_test:/timer \
-B ${scripts}/denoising_comp.py:/scripts/denoising_comp.py \
${base_dir}/singularity_images/dipy_testbed.sif \
/datain/bids/derivatives/dipy_denoising/${subject} ${subject}

        NOW=$(date "+%D-%T")
        echo "$1 finished $NOW" >> ${scripts}/dyno_$1_test_${inputNo}.txt
        exit 0
elif [ ${#SLURM_ARRAY_TASK_ID} == 3 ];
then
        inputNo="${SLURM_ARRAY_TASK_ID}"
	subject="sub-${proj}${inputNo}"
        echo "$1 started $NOW" > ${scripts}/dyno_$1_test_${inputNo}.txt

singularity run --cleanenv -B ${projDir}:/datain,${projDir}/denoising_test:/timer \
-B ${scripts}/denoising_comp.py:/scripts/denoising_comp.py \
${base_dir}/singularity_images/dipy_testbed.sif \
/datain/bids/derivatives/dipy_denoising/${subject} ${subject}

        NOW=$(date "+%D-%T")
        echo "$1 finished $NOW" >> ${scripts}/dyno_$1_test_${inputNo}.txt
        exit 0
fi
