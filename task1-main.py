import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os


def load_raw_kspace(path):
    k_space = np.load(path)
    return k_space


def recon_fft(raw_kspace):
    image = np.fft.fftn(raw_kspace)
    #plt.imshow(np.abs(image[:, :, 40]))
    for i in range(0, image.shape[2]):
        image[:, :, i] = np.rot90(np.rot90(image[:, :, i].transpose()))
    print(image.shape)
    #plt.figure(dpi=200)
    #plt.imshow(np.abs(image[:, :, 40]))
    #plt.show()
    return np.abs(image)


def save_nifti(recon_image, voxel_size, output_file_name):
    #hdr = nib.Nifti1Header()

    affine = np.array([[voxel_size[0], 0, 0, 0],
                       [0, voxel_size[1], 0, 0],
                       [0, 0, voxel_size[2], 0],
                       [0, 0, 0, 1]])
    img = nib.Nifti1Image(recon_image,  affine)
    print(img.header.get_zooms())
    nib.save(img, output_file_name)
    return voxel_size


# Input/Output files
raw_kspace_file = 'raw-kspace.npy'
output_file_name = 'recon-image.nii'
fov = np.array([200, 150, 80])

## Step 1 - Load raw kspace
raw_data = load_raw_kspace(raw_kspace_file)

## Step 2 - 3D FFT reconstruction
image = recon_fft(raw_data)
num_pixels = image.shape
voxel_size = np.divide(fov, num_pixels)

## Step 3 - Save to nifti format
save_nifti(image, voxel_size, output_file_name) # voxel size we acqure from FOV/num pixels and then save it to the voxel size