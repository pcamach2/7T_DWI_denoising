# Description: This script compares the denoising methods in DIPY
# Author: Paul B Camacho

# import libraries
import numpy as np
from dipy.data import get_fnames
from dipy.io.image import load_nifti, save_nifti
import matplotlib.pyplot as plt

from dipy.denoise.patch2self import patch2self
from dipy.denoise.nlmeans import nlmeans
from dipy.denoise.localpca import localpca
from dipy.denoise.localpca import mppca
from dipy.denoise.noise_estimate import estimate_sigma
from dipy.denoise.pca_noise_estimate import pca_noise_estimate
from dipy.core.gradients import gradient_table
import sys


# output directory from positional arguments
output_dir = sys.argv[1]
subject = sys.argv[2]
# data directory
data_dir = "/datain/sourcedata"
# replace these with CUPS data
dwi_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.nii.gz'
bval_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.bval'
bvec_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.bvec'
data, affine = load_nifti(dwi_fname)
bvals = np.loadtxt(bval_fname)
sigma = estimate_sigma(data)
gtab = gradient_table(bvals, bvec_fname)
pca_sigma = pca_noise_estimate(data, gtab)
denoised_arr_p2s = patch2self(data, bvals, model='ols', shift_intensity=True, patch_radius=2,
                          clip_negative_vals=False, b0_threshold=50)
denoised_arr_nlmeans = nlmeans(data, sigma=sigma, mask=None,
                            patch_radius=1, block_radius=1, rician=True,
                            num_threads=1)
denoised_arr_lpca = localpca(data, sigma=pca_sigma, patch_radius=2,
                            block_radius=1, rician=True, tau_factor=2.3,
                            pca_method='eig', out_dtype=np.float64)
denoised_arr_mppca, mppca_sigma = mppca(data, return_sigma=True, patch_radius=2,
                            block_radius=1, rician=True, tau_factor=2.3,
                            out_dtype=np.float64)

# Gets the center slice and the middle volume of the 4D diffusion data.
sli = data.shape[2] // 2
gra = 60  # pick out a random volume for a particular gradient direction

orig = data[:, :, sli, gra]
den_p2s = denoised_arr_p2s[:, :, sli, gra]
den_nlmeans = denoised_arr_nlmeans[:, :, sli, gra]
den_lpca = denoised_arr_lpca[:, :, sli, gra]
den_mppca = denoised_arr_mppca[:, :, sli, gra]

# computes the residuals
rms_diff_p2s = np.sqrt((orig - den_p2s) ** 2)
rms_diff_nlmeans = np.sqrt((orig - den_nlmeans) ** 2)
rms_diff_lpca = np.sqrt((orig - den_lpca) ** 2)
rms_diff_mppca = np.sqrt((orig - den_mppca) ** 2)

fig, axs = plt.subplots(2, 4, figsize=(16, 8),
                        subplot_kw={'xticks': [], 'yticks': []})

fig.subplots_adjust(hspace=0.3, wspace=0.05)

axs[0, 0].imshow(orig.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[0, 0].set_title('Original')
axs[0, 1].imshow(den_p2s.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[0, 1].set_title('Patch2Self')
axs[0, 2].imshow(den_nlmeans.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[0, 2].set_title('NLMeans')
axs[0, 3].imshow(den_lpca.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[0, 3].set_title('LocalPCA')
axs[1, 1].imshow(den_mppca.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[1, 1].set_title('MPPCA')
axs[1, 0].imshow(rms_diff_p2s.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[1, 0].set_title('Patch2Self Residuals')
axs[1, 2].imshow(rms_diff_nlmeans.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[1, 2].set_title('NLMeans Residuals')
axs[1, 3].imshow(rms_diff_lpca.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[1, 3].set_title('LocalPCA Residuals')
axs[1, 1].imshow(rms_diff_mppca.T, cmap='gray', interpolation='none',
                  origin='lower')
axs[1, 1].set_title('MPPCA Residuals')

fig.savefig('/out/denoised_comparison.png')

print("The result saved in denoised_comparison.png")


save_nifti('/out/denoised_patch2self.nii.gz', denoised_arr_p2s, affine)
save_nifti('/out/denoised_nlmeans.nii.gz', denoised_arr_nlmeans, affine)
save_nifti('/out/denoised_lpca.nii.gz', denoised_arr_lpca, affine)
save_nifti('/out/denoised_mppca.nii.gz', denoised_arr_mppca, affine)

print("Entire denoised data saved in denoised_patch2self.nii.gz")

# Write noise estimates to file
save_nifti("/out/sigma.nii.gz", sigma, affine)
save_nifti("/out/pca_sigma.nii.gz", pca_sigma, affine)
save_nifti("/out/mppca_sigma.nii.gz", mppca_sigma, affine) 
