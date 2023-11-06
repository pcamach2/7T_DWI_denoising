# Comparison of denoising methods for 7T DWI

Speed tests compare Patch2Self and [Patch2Self Parallel (WIP)](https://github.com/ShreyasFadnavis/p2s_parallel)

Patch2Self denoising example:

![sub-CUPS003_patch2self_parallel_20_denoised_comparison](https://github.com/pcamach2/7T_DWI_denoising/blob/main/sub-CUPS003_patch2self_parallel_20_denoised_comparison.png)

Comparison with NLMEANS, LPCA, and MP-PCA

![sub-CUPS003_patch2self_20_denoised_comparison.png](https://github.com/pcamach2/7T_DWI_denoising/blob/main/sub-CUPS003_patch2self_20_denoised_comparison.png)

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

