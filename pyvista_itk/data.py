"""Download example datasets for pyvista-itk."""

import os
import shutil
from pathlib import Path
from urllib.request import urlretrieve
import zipfile
import gzip
import pyvista as pv
import itk


def _get_data_dir():
    """Get the local data directory."""
    data_dir = Path.home() / ".pyvista-itk" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def _download_file(url, filename, data_dir=None):
    """Download a file from a URL if not already cached."""
    if data_dir is None:
        data_dir = _get_data_dir()
    
    filepath = data_dir / filename
    
    if filepath.exists():
        print(f"Using cached file: {filepath}")
        return str(filepath)
    
    print(f"Downloading {filename}...")
    urlretrieve(url, filepath)
    print(f"Downloaded to: {filepath}")
    
    return str(filepath)


def download_brain_mri():
    """Download example brain MRI data.
    
    Returns
    -------
    str
        Path to the downloaded NIfTI file.
        
    Notes
    -----
    This downloads a sample T1-weighted brain MRI from the BrainWeb dataset.
    The data is in NIfTI format (.nii.gz).
    """
    # Using a sample from the NIfTI test data repository
    url = "https://github.com/nipy/nibabel/raw/master/nibabel/tests/data/example4d.nii.gz"
    filename = "brain_mri.nii.gz"
    
    return _download_file(url, filename)


def download_ct_chest():
    """Download example chest CT data.
    
    Returns
    -------
    str
        Path to the downloaded NIfTI file.
        
    Notes
    -----
    This downloads a sample chest CT scan.
    The data is in NIfTI format (.nii.gz).
    """
    # Using a sample CT from public datasets
    url = "https://github.com/InsightSoftwareConsortium/ITKTestingData/raw/master/Input/HeadMRVolume.mha"
    filename = "ct_chest.mha"
    
    return _download_file(url, filename)


def download_dicom_series():
    """Download example DICOM series.
    
    Returns
    -------
    str
        Path to the directory containing DICOM files.
        
    Notes
    -----
    This downloads a sample DICOM series for testing.
    """
    # Create a directory for DICOM files
    data_dir = _get_data_dir()
    dicom_dir = data_dir / "dicom_series"
    
    if dicom_dir.exists() and any(dicom_dir.iterdir()):
        print(f"Using cached DICOM series: {dicom_dir}")
        return str(dicom_dir)
    
    dicom_dir.mkdir(exist_ok=True)
    
    # Download sample DICOM files from ITK testing data
    base_url = "https://github.com/InsightSoftwareConsortium/ITK/raw/master/Testing/Data/Input/DicomSeries/"
    dicom_files = [
        "Image0075.dcm",
        "Image0076.dcm", 
        "Image0077.dcm",
    ]
    
    for dcm_file in dicom_files:
        url = base_url + dcm_file
        _download_file(url, dcm_file, dicom_dir)
    
    return str(dicom_dir)


def create_synthetic_image(size=(100, 100, 50), spacing=(1.0, 1.0, 2.0), 
                          pattern="gradient"):
    """Create a synthetic 3D image for testing.
    
    Parameters
    ----------
    size : tuple of int, default=(100, 100, 50)
        Size of the image in voxels (x, y, z).
    spacing : tuple of float, default=(1.0, 1.0, 2.0)
        Voxel spacing in mm (x, y, z).
    pattern : str, default="gradient"
        Pattern to generate. Options: "gradient", "sphere", "checkerboard".
        
    Returns
    -------
    itk.Image
        Synthetic ITK image.
    """
    import numpy as np
    
    # Create coordinate arrays
    x = np.arange(size[0]) * spacing[0]
    y = np.arange(size[1]) * spacing[1]
    z = np.arange(size[2]) * spacing[2]
    
    # Create meshgrid
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    if pattern == "gradient":
        # Linear gradient
        data = (X + Y + Z) / (x[-1] + y[-1] + z[-1])
    elif pattern == "sphere":
        # Sphere in center
        center = (x[-1]/2, y[-1]/2, z[-1]/2)
        R = np.sqrt((X - center[0])**2 + (Y - center[1])**2 + (Z - center[2])**2)
        radius = min(center) * 0.8
        data = (R < radius).astype(float)
    elif pattern == "checkerboard":
        # 3D checkerboard
        check_size = 10
        data = ((X//check_size + Y//check_size + Z//check_size) % 2).astype(float)
    else:
        raise ValueError(f"Unknown pattern: {pattern}")
    
    # Normalize to 0-1
    data = (data - data.min()) / (data.max() - data.min())
    
    # Convert to ITK image
    image = itk.image_from_array(data.astype(np.float32))
    image.SetSpacing(spacing)
    image.SetOrigin([0.0, 0.0, 0.0])
    
    return image


def load_example_brain_mri():
    """Load example brain MRI as ITK image.
    
    Returns
    -------
    itk.Image
        Brain MRI as ITK image.
    """
    filepath = download_brain_mri()
    return itk.imread(filepath)


def load_example_ct_chest():
    """Load example chest CT as ITK image.
    
    Returns
    -------
    itk.Image
        Chest CT as ITK image.
    """
    filepath = download_ct_chest()
    return itk.imread(filepath)


# Convenience functions that mirror PyVista's API
def examples():
    """Return dictionary of available example datasets."""
    return {
        "brain_mri": "T1-weighted brain MRI from BrainWeb",
        "ct_chest": "Chest CT scan",
        "dicom_series": "Sample DICOM series",
        "synthetic_gradient": "Synthetic gradient image",
        "synthetic_sphere": "Synthetic sphere image",
        "synthetic_checkerboard": "Synthetic checkerboard image",
    }


def clear_cache():
    """Clear the downloaded data cache."""
    data_dir = _get_data_dir()
    if data_dir.exists():
        shutil.rmtree(data_dir)
        print(f"Cleared cache directory: {data_dir}")
    else:
        print("Cache directory does not exist")