"""Conversion functions from PyVista to ITK."""

import itk
import pyvista as pv
import numpy as np


def pyvista_grid_to_itk_image(grid: pv.ImageData) -> itk.Image:
    """Convert a PyVista ImageData to an ITK Image.
    
    Parameters
    ----------
    grid : pv.ImageData
        The PyVista ImageData to convert.
        
    Returns
    -------
    itk.Image
        An ITK image containing the grid data.
    """
    if not isinstance(grid, pv.ImageData):
        raise TypeError(f"Expected pv.ImageData, got {type(grid)}")
    
    if grid.n_arrays == 0:
        raise ValueError("No point data arrays found in the grid")
    
    arr = grid.point_data.active_scalars.reshape(grid.dimensions[::-1])
    
    image = itk.image_from_array(arr)
    image.SetSpacing(grid.spacing)
    image.SetOrigin(grid.origin)
    
    return image