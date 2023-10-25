#!/bin/bash
#
#SBATCH --job-name=CUPS_denoising_speedtest
#SBATCH --output=CUPS_denoising_speedtest.txt
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

singularity exec --cleanenv -B ${projDir}:/datain,${projDir}/denoising_test:/timer \
-B ${scripts}/denoising_speed_test_simple.py:/scripts/denoising_speed_test_simple.py \
-B ${scripts}/profiler.py:/scripts/profiler.py \
${base_dir}/singularity_images/dipy_testbed.sif \
python3 /scripts/profiler.py ${subject} 'patch2self_parallel' 15 '/datain/bids/derivatives/dipy_denoising'

	NOW=$(date "+%D-%T")
	echo "$1 finished $NOW" >> ${scripts}/dyno_$1_test_${inputNo}.txt
	exit 0
elif [ ${#SLURM_ARRAY_TASK_ID} == 2 ];
then
        inputNo="0${SLURM_ARRAY_TASK_ID}"
	subject="sub-${proj}${inputNo}"
        echo "$1 started $NOW" > ${scripts}/dyno_$1_test_${inputNo}.txt
	
singularity exec --cleanenv -B ${projDir}:/datain,${projDir}/denoising_test:/timer \
-B ${scripts}/denoising_speed_test_simple.py:/scripts/denoising_speed_test_simple.py \
-B ${scripts}/profiler.py:/scripts/profiler.py \
${base_dir}/singularity_images/dipy_testbed.sif \
python3 /scripts/profiler.py ${subject} 'patch2self_parallel' 15 '/datain/bids/derivatives/dipy_denoising'

        NOW=$(date "+%D-%T")
        echo "$1 finished $NOW" >> ${scripts}/dyno_$1_test_${inputNo}.txt
        exit 0
elif [ ${#SLURM_ARRAY_TASK_ID} == 3 ];
then
        inputNo="${SLURM_ARRAY_TASK_ID}"
	subject="sub-${proj}${inputNo}"
        echo "$1 started $NOW" > ${scripts}/dyno_$1_test_${inputNo}.txt

singularity exec --cleanenv -B ${projDir}:/datain,${projDir}/denoising_test:/timer \
-B ${scripts}/denoising_speed_test_simple.py:/scripts/denoising_speed_test_simple.py \
-B ${scripts}/profiler.py:/scripts/profiler.py \
${base_dir}/singularity_images/dipy_testbed.sif \
python3 /scripts/profiler.py ${subject} 'patch2self_parallel' 15 '/datain/bids/derivatives/dipy_denoising'

        NOW=$(date "+%D-%T")
        echo "$1 finished $NOW" >> ${scripts}/dyno_$1_test_${inputNo}.txt
        exit 0
fi
