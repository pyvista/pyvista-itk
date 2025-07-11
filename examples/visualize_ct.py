"""Example: Visualizing CT data using PyVista-ITK."""

import itk
import pyvista as pv
from pyvista_itk import itk_image_to_pyvista_grid, pyvista_grid_to_itk_image, data


def visualize_ct_example():
    """Example demonstrating CT visualization workflow."""
    
    print("Creating a synthetic 3D image with ITK...")
    image = data.create_synthetic_image(
        size=[100, 100, 50],
        spacing=[1.0, 1.0, 2.0],
        pattern="gradient"
    )
    
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


def visualize_brain_mri_example():
    """Example demonstrating brain MRI visualization."""
    print("Loading example brain MRI...")
    image = data.load_example_brain_mri()
    
    print("Converting to PyVista...")
    grid = itk_image_to_pyvista_grid(image)
    
    print(f"Image dimensions: {grid.dimensions}")
    print(f"Image spacing: {grid.spacing}")
    
    print("Visualizing brain MRI...")
    plotter = pv.Plotter()
    plotter.add_volume(
        grid,
        cmap="gray",
        opacity="sigmoid",
        show_scalar_bar=True,
    )
    plotter.add_axes()
    plotter.view_isometric()
    plotter.show()


def visualize_with_threshold_example():
    """Example demonstrating visualization with thresholding."""
    print("Creating synthetic sphere image...")
    image = data.create_synthetic_image(pattern="sphere")
    
    print("Converting to PyVista...")
    grid = itk_image_to_pyvista_grid(image)
    
    print("Applying threshold...")
    thresholded = grid.threshold(0.5)
    
    print("Visualizing...")
    plotter = pv.Plotter()
    plotter.add_mesh(thresholded, color="red", opacity=0.8)
    plotter.add_mesh(grid.outline(), color="black")
    plotter.add_axes()
    plotter.show()


def process_and_visualize_example():
    """Example showing ITK processing followed by PyVista visualization."""
    print("Creating synthetic checkerboard image...")
    image = data.create_synthetic_image(
        size=[80, 80, 40],
        pattern="checkerboard"
    )
    
    print("Applying Gaussian smoothing with ITK...")
    smoothed = itk.smooth_recursive_gaussian_image_filter(
        image, 
        sigma=2.0
    )
    
    print("Converting both images to PyVista...")
    original_grid = itk_image_to_pyvista_grid(image)
    smoothed_grid = itk_image_to_pyvista_grid(smoothed)
    
    print("Visualizing side by side...")
    plotter = pv.Plotter(shape=(1, 2))
    
    plotter.subplot(0, 0)
    plotter.add_text("Original", position="upper_edge")
    plotter.add_volume(original_grid, cmap="viridis")
    plotter.add_axes()
    
    plotter.subplot(0, 1)
    plotter.add_text("Smoothed", position="upper_edge")
    plotter.add_volume(smoothed_grid, cmap="viridis")
    plotter.add_axes()
    
    plotter.link_views()
    plotter.show()


if __name__ == "__main__":
    import sys
    
    examples = {
        "1": ("Synthetic gradient visualization", visualize_ct_example),
        "2": ("Brain MRI visualization", visualize_brain_mri_example),
        "3": ("Threshold visualization", visualize_with_threshold_example),
        "4": ("ITK processing + PyVista visualization", process_and_visualize_example),
    }
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice in examples:
            print(f"\n{examples[choice][0]}")
            print("-" * 40)
            examples[choice][1]()
        else:
            print(f"Invalid choice. Available options: {list(examples.keys())}")
    else:
        print("\nAvailable examples:")
        for key, (desc, _) in examples.items():
            print(f"  {key}: {desc}")
        print("\nRun with: python visualize_ct.py <number>")
        print("\nRunning default example...")
        visualize_ct_example()