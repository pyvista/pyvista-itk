"""Example: Visualizing CT data using PyVista-ITK."""

import itk
import pyvista as pv
from pyvista_itk import itk_image_to_pyvista_grid, pyvista_grid_to_itk_image


def visualize_ct_example():
    """Example demonstrating CT visualization workflow."""
    
    print("Creating a synthetic 3D image with ITK...")
    image_type = itk.Image[itk.F, 3]
    image = image_type.New()
    
    size = [100, 100, 50]
    index = [0, 0, 0]
    region = itk.ImageRegion[3]()
    region.SetSize(size)
    region.SetIndex(index)
    
    image.SetRegions(region)
    image.SetSpacing([1.0, 1.0, 2.0])
    image.SetOrigin([0.0, 0.0, 0.0])
    image.Allocate()
    
    print("Filling image with gradient values...")
    for z in range(size[2]):
        for y in range(size[1]):
            for x in range(size[0]):
                value = (x + y + z) / 3.0
                image.SetPixel([x, y, z], value)
    
    print("Converting ITK image to PyVista grid...")
    grid = itk_image_to_pyvista_grid(image)
    
    print(f"Grid dimensions: {grid.dimensions}")
    print(f"Grid spacing: {grid.spacing}")
    print(f"Grid origin: {grid.origin}")
    
    print("Converting back to ITK image...")
    image_back = pyvista_grid_to_itk_image(grid)
    
    print("Visualizing with PyVista...")
    plotter = pv.Plotter()
    plotter.add_volume(
        grid,
        cmap="bone",
        opacity="sigmoid",
        show_scalar_bar=True,
    )
    plotter.add_axes()
    plotter.show_grid()
    plotter.show()


def load_dicom_example(dicom_directory=None):
    """Example for loading and visualizing DICOM data.
    
    Parameters
    ----------
    dicom_directory : str, optional
        Path to directory containing DICOM files.
    """
    if dicom_directory is None:
        print("Please provide a DICOM directory path")
        return
    
    print(f"Loading DICOM series from: {dicom_directory}")
    
    names_generator = itk.GDCMSeriesFileNames.New()
    names_generator.SetUseSeriesDetails(True)
    names_generator.SetDirectory(dicom_directory)
    
    series_uids = names_generator.GetSeriesUIDs()
    
    if not series_uids:
        print("No DICOM series found in the directory")
        return
    
    print(f"Found {len(series_uids)} series")
    series_uid = series_uids[0]
    
    file_names = names_generator.GetFileNames(series_uid)
    
    pixel_type = itk.F
    dimension = 3
    image_type = itk.Image[pixel_type, dimension]
    
    reader = itk.ImageSeriesReader[image_type].New()
    reader.SetFileNames(file_names)
    reader.Update()
    
    image = reader.GetOutput()
    
    print("Converting to PyVista...")
    grid = itk_image_to_pyvista_grid(image)
    
    print("Visualizing...")
    plotter = pv.Plotter()
    plotter.add_volume(
        grid,
        cmap="bone",
        opacity="sigmoid",
        show_scalar_bar=True,
    )
    plotter.add_axes()
    plotter.show_grid()
    plotter.view_isometric()
    plotter.show()


if __name__ == "__main__":
    visualize_ct_example()