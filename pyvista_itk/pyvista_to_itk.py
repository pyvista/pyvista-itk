"""Conversion functions from PyVista to ITK."""

import itk
import pyvista as pv
import numpy as np


def pyvista_grid_to_itk_image(grid: pv.UniformGrid) -> itk.Image:
    """Convert a PyVista UniformGrid to an ITK Image.
    
    Parameters
    ----------
    grid : pv.UniformGrid
        The PyVista UniformGrid to convert.
        
    Returns
    -------
    itk.Image
        An ITK image containing the grid data.
    """
    if not isinstance(grid, pv.UniformGrid):
        raise TypeError(f"Expected pv.UniformGrid, got {type(grid)}")
    
    if grid.n_arrays == 0:
        raise ValueError("No point data arrays found in the grid")
    
    arr = grid.point_data.active_scalars.reshape(grid.dimensions[::-1])
    
    image = itk.image_from_array(arr)
    image.SetSpacing(grid.spacing)
    image.SetOrigin(grid.origin)
    
    return image