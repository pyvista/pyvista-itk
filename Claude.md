# pyvista-itk

`pyvista-itk` is a Python library designed to enable seamless interoperability between PyVista and ITK (Insight Toolkit).

## Goals

- Convert `itk.Image` to `pyvista.UniformGrid` for 3D visualization
- Convert `pyvista.UniformGrid` to `itk.Image` for image processing
- Enable visualization and analysis of medical imaging data using PyVista
- Provide examples for working with DICOM, CT, MRI data

## Project Structure

```
pyvista-itk/
├── pyvista_itk/
│   ├── __init__.py
│   ├── itk_to_pyvista.py
│   ├── pyvista_to_itk.py
├── examples/
│   ├── visualize_ct.py
├── tests/
│   ├── test_conversions.py
├── README.md
├── pyproject.toml
└── LICENSE
```

## Sample Conversion: ITK to PyVista

```python
import itk
import pyvista as pv
import numpy as np

def itk_image_to_pyvista_grid(image: itk.Image) -> pv.UniformGrid:
    arr = itk.GetArrayFromImage(image)
    spacing = image.GetSpacing()
    origin = image.GetOrigin()
    return pv.UniformGrid(dims=arr.shape[::-1], spacing=spacing, origin=origin, scalars=arr)
```

## Sample Conversion: PyVista to ITK

```python
def pyvista_grid_to_itk_image(grid: pv.UniformGrid) -> itk.Image:
    arr = grid.point_data.active_scalars.reshape(grid.dimensions[::-1])
    image = itk.image_from_array(arr)
    image.SetSpacing(grid.spacing)
    image.SetOrigin(grid.origin)
    return image
```

## Next Steps

1. Create GitHub repository
2. Add dependencies: `pyvista`, `itk`, `numpy`
3. Implement conversion functions
4. Add test coverage using `pytest`
5. Provide visualization examples
6. Publish on PyPI and/or document via GitHub Pages
