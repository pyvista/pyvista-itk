from pyvista_itk import itk_image_to_pyvista_grid, data

# Download and load example brain MRI
image = data.load_example_brain_mri()

# Convert to PyVista for visualization
grid = itk_image_to_pyvista_grid(image)

# Print grid info instead of plotting
print(f"Successfully converted ITK image to PyVista grid!")
print(f"Grid type: {type(grid)}")
print(f"Grid dimensions: {grid.dimensions}")
print(f"Grid spacing: {grid.spacing}")
print(f"Grid origin: {grid.origin}")
print(f"Number of points: {grid.n_points}")
print(f"Number of cells: {grid.n_cells}")
print(f"Point data arrays: {list(grid.point_data.keys())}")
