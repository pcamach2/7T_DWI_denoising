import matplotlib.pyplot as plt
from PIL import Image

from typing import List
from PIL import Image
import matplotlib.pyplot as plt

def create_mosaic(a: List[str], b: List[str], c: List[str], plots_dir: str) -> None:
    """
    Creates a mosaic of images by opening and appending images from the specified file paths, and saving the resulting
    mosaic to a file.

    Args:
        a (List[str]): A list of strings representing the first part of the file name for each image.
        b (List[str]): A list of strings representing the second part of the file name for each image.
        c (List[str]): A list of strings representing the third part of the file name for each image.
        plots_dir (str): A string representing the directory where the plots are located.

    Returns:
        None
    """
    images = []
    for i in range(len(a)):
        for ii in range(len(b)):
            for iii in range(len(c)):
                img = Image.open(f'{plots_dir}/{a[i]}_{b[ii]}_distribution_{c[iii]}.png')
                images.append(img)

    # print(images)
   
    num_rows = len(a) 
    num_cols = len(b) * 2
    num_images = len(images)
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 8))
    fig.subplots_adjust(wspace=0.1, hspace=0.1)
    
    for i in range(num_rows):
        for j in range(num_cols):
            index = i * num_cols + j
            if index < num_images:
                if i < num_rows/2:
                    axs[i, j].imshow(images[index])
                    axs[i, j].axis('off')
                    axs[i, j].text(-0.07, 0.95, chr(97+index), transform=axs[i, j].transAxes, fontsize=10, va='top', ha='left')
                else:
                    axs[i, j].imshow(images[index])
                    axs[i, j].axis('off')
                    axs[i, j].text(-0.05, 0.99, chr(97+index), transform=axs[i, j].transAxes, fontsize=10, va='top', ha='left')
    
    plt.savefig(f'{plots_dir}/mosaic.png', bbox_inches='tight', pad_inches=0, dpi=1200)
    plt.close()

# Cingulum_Frontal_Parietal_L_dti_fa_distribution_128d.png

if __name__ == '__main__':
    a = ['Corpus_Callosum_Body', 'Corpus_Callosum_Forceps_Major', 'Corticospinal_Tract_L', 'Corticospinal_Tract_R']
    b = ['dti_fa', 'md', 'mean_length_mm']
    c = ['60d', '128d']
    plots_dir = '/plots'
    create_mosaic(a, b, c, plots_dir)
