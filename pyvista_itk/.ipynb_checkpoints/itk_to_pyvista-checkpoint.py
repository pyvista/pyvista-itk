"""Conversion functions from ITK to PyVista."""

import itk
import pyvista as pv
import numpy as np


def itk_image_to_pyvista_grid(image: itk.Image) -> pv.ImageData:
    """Convert an ITK Image to a PyVista ImageData.
    
    Parameters
    ----------
    image : itk.Image
        The ITK image to convert.
        
    Returns
    -------
    pv.ImageData
        A PyVista ImageData containing the image data.
    """
    arr = itk.GetArrayFromImage(image)
    spacing = tuple(image.GetSpacing())
    origin = tuple(image.GetOrigin())
    
    # Handle 4D images by taking the first volume
    if arr.ndim == 4:
        arr = arr[0]
        spacing = spacing[:3]
        origin = origin[:3]
    
    grid = pv.ImageData(
        dimensions=arr.shape[::-1],
        spacing=spacing,
        origin=origin
    )
    
    grid.point_data["scalars"] = arr.flatten(order="F")
    
    return grid