# Comparison of denoising methods for 7T DWI

Speed tests compare Patch2Self and [Patch2Self Parallel (WIP)](https://github.com/ShreyasFadnavis/p2s_parallel)

Patch2Self denoising example:

![sub-CUPS064_patch2self_parallel_15_denoised_comparison](https://github.com/pcamach2/7T_DWI_denoising/assets/49655443/0a3e300f-ffc5-412b-a5a7-4f823ca1eecd)

Comparison with NLMEANS, LPCA, and MP-PCA

![denoised_comparison](https://github.com/pcamach2/7T_DWI_denoising/assets/49655443/610793a9-a9e9-436d-8398-e13435b55025)

## Guide

Copy sourcedata from original project to each <Project>_<method>:
```
cp -R testing/CUPS/bids/sourcedata CUPS_lpca/bids/ && cp -R testing/CUPS/bids/sourcedata CUPS_mppca/bids/ && cp -R testing/CUPS/bids/sourcedata CUPS_nlmeans/bids/ && cp -R testing/CUPS/bids/sourcedata CUPS_p2s/bids/
```

Denoise with each method for participants with IDs in sbatch array:
```
sbatch -a 001,029,060 ./dyno_CUPS_denoising_comp.sh CUPS /home/projects/BICpipeline terra
```

Run QSIPrep preprocessing without a denoising step:
```
sbatch -a 1 ./slurm_proc_7T_qsiprep_nodenoise.sh -p CUPS_lpca -s A -z CUPS060 -b /path/to/pipelines -t terra
sbatch -a 1 ./slurm_proc_7T_qsiprep_nodenoise.sh -p CUPS_mppca -s A -z CUPS060 -b /path/to/pipelines -t terra
sbatch -a 1 ./slurm_proc_7T_qsiprep_nodenoise.sh -p CUPS_p2s -s A -z CUPS060 -b /path/to/pipelines -t terra
sbatch -a 1 ./slurm_proc_7T_qsiprep_nodenoise.sh -p CUPS_nlmeans -s A -z CUPS060 -b /path/to/pipelines -t terra
```

Copy sourcedata from original project to each <Project>_<method>:
```
for i in sub-CUPS060; do mv dipy_denoising/${i}/denoised_patch2self.nii.gz /path/to/projects_dir/CUPS_p2s/bids/sourcedata/${i}/ses-A/dwi/${i}_ses-A_run-1_dwi.nii.gz && mv dipy_denoising/${i}/denoised_lpca.nii.gz /path/to/projects_dir/CUPS_lpca/bids/sourcedata/${i}/ses-A/dwi/${i}_ses-A_run-1_dwi.nii.gz && mv dipy_denoising/${i}/denoised_mppca.nii.gz /path/to/projects_dir/CUPS_mppca/bids/sourcedata/${i}/ses-A/dwi/${i}_ses-A_run-1_dwi.nii.gz && mv dipy_denoising/${i}/denoised_nlmeans.nii.gz /path/to/projects_dir/CUPS_nlmeans/bids/sourcedata/${i}/ses-A/dwi/${i}_ses-A_run-1_dwi.nii.gz; done
```

Run QSIPrep reconstruction:
```
sbatch -a 1 ./slurm_proc_qsirecon_dsistudio_autotrack.sh -p CUPS_lpca -s A -z CUPS060 -b /path/to/pipelines -t terra
sbatch -a 1 ./slurm_proc_qsirecon_dsistudio_autotrack.sh -p CUPS_mppca -s A -z CUPS060 -b /path/to/pipelines -t terra
sbatch -a 1 ./slurm_proc_qsirecon_dsistudio_autotrack.sh -p CUPS_p2s -s A -z CUPS060 -b /path/to/pipelines -t terra
sbatch -a 1 ./slurm_proc_qsirecon_dsistudio_autotrack.sh -p CUPS_nlmeans -s A -z CUPS060 -b /path/to/pipelines -t terra
```

After obtaining all AutoTrack files from QSIPrep `dsi_studio_autotrack` workflow in `/path/to/projects_dir`, where the parent directories for all <Project>_<method> included: 
```
 python3 process_autotrack_csvs.py /path/to/projects_dir
```

``` 
 python3 get_tract_dfs.py /path/to/results
 
 python3 plot_distributions.py /path/to/results/bundle_dfs
 
 python3 mosaic.py /path/to/results/plots
```

## PyAFQ Tractometry - (WIP)

### Patch2Self
![Screenshot from 2023-10-29 16-26-08](https://github.com/pcamach2/7T_DWI_denoising/assets/49655443/60ff6ebd-91de-4d41-b875-bc9513048009)

### NLMEANS
![Screenshot from 2023-10-29 16-28-55](https://github.com/pcamach2/7T_DWI_denoising/assets/49655443/790c1c01-3a6f-412f-9f06-ba65c417fc56)

### LPCA
![Screenshot from 2023-10-29 16-28-29](https://github.com/pcamach2/7T_DWI_denoising/assets/49655443/d30b061d-fe49-4e83-b547-868e03db39c9)

### MP-PCA
![Screenshot from 2023-10-29 16-26-13](https://github.com/pcamach2/7T_DWI_denoising/assets/49655443/cde7925d-a89f-4b4c-bf9f-04ec9eb24d18)

