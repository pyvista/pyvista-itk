"""Conversion functions from ITK to PyVista."""

import itk
import pyvista as pv
import numpy as np


def itk_image_to_pyvista_grid(image: itk.Image) -> pv.UniformGrid:
    """Convert an ITK Image to a PyVista UniformGrid.
    
    Parameters
    ----------
    image : itk.Image
        The ITK image to convert.
        
    Returns
    -------
    pv.UniformGrid
        A PyVista UniformGrid containing the image data.
    """
    arr = itk.GetArrayFromImage(image)
    spacing = image.GetSpacing()
    origin = image.GetOrigin()
    
    grid = pv.UniformGrid(
        dims=arr.shape[::-1],
        spacing=spacing,
        origin=origin
    )
    
    grid.point_data["scalars"] = arr.flatten(order="F")
    
    return grid