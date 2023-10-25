# Description: This script performs the patch2self paralell denoising method
#              and gives the execution time and the denoised data.
# please reference DIPY if you use this script.
# Usage: python denoising_speed_test.py <output_dir> <subject> <denoising_method> <n_jobs>
# Author: Paul B Camacho

# import libraries
import sys
import numpy as np

from dipy.io.image import load_nifti, save_nifti
import matplotlib.pyplot as plt
from dipy.segment.mask import median_otsu
from dipy.reconst.dti import TensorModel
from dipy.io.gradients import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from scipy.ndimage import binary_dilation
from dipy.segment.mask import segment_from_cfa
from dipy.segment.mask import bounding_box


# output directory from positional arguments
output_dir = sys.argv[1]
subject = sys.argv[2]
method = sys.argv[3] # denoising method (patch2self or patch2self_parallel)
n_jobs = int(sys.argv[4]) # number of jobs for parallel processing

print("method: " + method)

if method == "patch2self":
    from dipy.denoise.patch2self import patch2self
elif method == "patch2self_parallel":
    from p2s_parallel import patch2self
else:
    print("Invalid denoising method. Please use 'patch2self' or 'patch2self_parallel'")


# data directory
data_dir = "/datain/bids/sourcedata"
# replace these with CUPS data
dwi_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.nii.gz'
bval_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.bval'
bvec_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.bvec'
data, affine = load_nifti(dwi_fname)
bvals,bvecs =read_bvals_bvecs(bval_fname, bvec_fname)
gtab = gradient_table(bvals, bvec_fname)

# instantiate the denoised array
denoised_arr_p2s = np.zeros(data.shape)
if method == "patch2self":
    denoised_arr_p2s = patch2self(data, bvals, model='ridge',
                              shift_intensity=True,
                              clip_negative_vals=False,
                              b0_threshold=50, verbose=True,
                              alpha=0)
elif method == "patch2self_parallel":
    denoised_arr_p2s = patch2self(data, bvals, model='ridge',
                          shift_intensity=True,
                          clip_negative_vals=False,
                          b0_threshold=50, verbose=True,
                          n_jobs=n_jobs, alpha=0)

# Gets the center slice and the middle volume of the 4D diffusion data.
sli = data.shape[2] // 2
gra = 60  # pick out a random volume for a particular gradient direction

orig = data[:, :, sli, gra]
den_p2s = denoised_arr_p2s[:, :, sli, gra]

# computes the residuals
rms_diff_p2s = np.sqrt((orig - den_p2s) ** 2)

fig, axs = plt.subplots(1, 3, figsize=(16, 8),
                        subplot_kw={'xticks': [], 'yticks': []})

fig.subplots_adjust(hspace=0.3, wspace=0.05)

axs[0].imshow(orig.T, cmap='gray', interpolation='none',
              origin='lower')
axs[0].set_title('Original')
axs[1].imshow(den_p2s.T, cmap='gray', interpolation='none',
              origin='lower')
axs[1].set_title('Patch2Self')
axs[2].imshow(rms_diff_p2s.T, cmap='gray', interpolation='none',
              origin='lower')
axs[2].set_title('Patch2Self Residuals')

fig.savefig(output_dir + "/" + subject + "_" + method + "_" + str(n_jobs) + "_denoised_comparison.png")
print("The result saved in denoised_comparison.png")
save_nifti(output_dir + "/" + subject + "_" + method + "_" + str(n_jobs) + "_denoised_patch2self.nii.gz", denoised_arr_p2s, affine)
print("Entire denoised data saved in denoised_patch2self.nii.gz")

