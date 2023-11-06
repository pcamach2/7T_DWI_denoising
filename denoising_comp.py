# Description: This script compares the denoising methods in DIPY
# Author: Paul B Camacho

# import libraries
import numpy as np
import matplotlib.pyplot as plt
# from dipy.denoise.patch2self import patch2self
from dipy.io.image import load_nifti, save_nifti
from dipy.denoise.nlmeans import nlmeans
from dipy.denoise.localpca import localpca
from dipy.denoise.localpca import mppca
from dipy.denoise.noise_estimate import estimate_sigma
from dipy.denoise.pca_noise_estimate import pca_noise_estimate
from dipy.core.gradients import gradient_table
import sys

# import the p2s_parallel.py script
from p2s_parallel import patch2self
import numpy as np

def compare_denoising_methods(output_dir:str, subject:str, N_JOBS:int):
    """
    This function compares the denoising methods in DIPY.
    
    Parameters:
    output_dir (str): The output directory.
    subject (str): The name of the subject.
    N_JOBS (int): The number of jobs to run in parallel.
    
    Returns:
    None
    """
    # data directory
    data_dir = "/datain/sourcedata"
    # replace these with CUPS data
    dwi_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.nii.gz'
    bval_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.bval'
    bvec_fname = data_dir + '/' + subject + '/ses-A/dwi/' + subject + '_ses-A_run-1_dwi.bvec'
    # load the diffusion data
    data, affine = load_nifti(dwi_fname)
    bvals = np.loadtxt(bval_fname)
    sigma = estimate_sigma(data)
    gtab = gradient_table(bvals, bvec_fname)
    pca_sigma = pca_noise_estimate(data, gtab)

    # denoise the data using patch2self
    denoised_arr_p2s = patch2self(data, bvals, model='ridge',
                                   shift_intensity=True,
                                   clip_negative_vals=False,
                                   b0_threshold=50, verbose=True,
                                   n_jobs=N_JOBS, alpha=0)

    # denoise the data using nlmeans
    denoised_arr_nlmeans = nlmeans(data, sigma=sigma, mask=None,
                                   patch_radius=1, block_radius=1, rician=True,
                                   num_threads=1)

    # denoise the data using localpca
    denoised_arr_lpca = localpca(data, sigma=pca_sigma, patch_radius=2,
                                  tau_factor=2.3, pca_method='eig', out_dtype=np.float64)

    # denoise the data using mppca
    denoised_arr_mppca, mppca_sigma = mppca(data, return_sigma=True, patch_radius=2,
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

    fig, axs = plt.subplots(2, 5, figsize=(16, 8),
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
    axs[0, 4].imshow(den_mppca.T, cmap='gray', interpolation='none',
                     origin='lower')
    axs[0, 4].set_title('MPPCA')

    axs[1, 1].imshow(rms_diff_p2s.T, cmap='gray', interpolation='none',
                     origin='lower')
    axs[1, 1].set_title('Patch2Self Residuals')
    axs[1, 2].imshow(rms_diff_nlmeans.T, cmap='gray', interpolation='none',
                     origin='lower')
    axs[1, 2].set_title('NLMeans Residuals')
    axs[1, 3].imshow(rms_diff_lpca.T, cmap='gray', interpolation='none',
                     origin='lower')
    axs[1, 3].set_title('LocalPCA Residuals')
    axs[1, 4].imshow(rms_diff_mppca.T, cmap='gray', interpolation='none',
                     origin='lower')
    axs[1, 4].set_title('MPPCA Residuals')
    axs[1, 0].axis('off')

    fig.suptitle('Comparison of Denoising Methods')

    fig.savefig(output_dir + '/denoised_comparison.png')

    print("The result saved in denoised_comparison.png")

    # save the residuals
    save_nifti(output_dir + '/residuals_p2s.nii.gz', rms_diff_p2s, affine)
    save_nifti(output_dir + '/residuals_nlmeans.nii.gz', rms_diff_nlmeans, affine)
    save_nifti(output_dir + '/residuals_lpca.nii.gz', rms_diff_lpca, affine)
    save_nifti(output_dir + '/residuals_mppca.nii.gz', rms_diff_mppca, affine)
