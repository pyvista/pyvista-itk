"""Tests for PyVista-ITK conversion functions."""

import pytest
import numpy as np
import itk
import pyvista as pv
from pyvista_itk import itk_image_to_pyvista_grid, pyvista_grid_to_itk_image


class TestConversions:
    """Test conversion functions between ITK and PyVista."""
    
    def create_test_itk_image(self, size=(10, 10, 10), spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0)):
        """Create a test ITK image with known properties."""
        image_type = itk.Image[itk.F, 3]
        image = image_type.New()
        
        region = itk.ImageRegion[3]()
        region.SetSize(list(size))
        region.SetIndex([0, 0, 0])
        
        image.SetRegions(region)
        image.SetSpacing(list(spacing))
        image.SetOrigin(list(origin))
        image.Allocate()
        
        for z in range(size[2]):
            for y in range(size[1]):
                for x in range(size[0]):
                    value = x + y * 10 + z * 100
                    image.SetPixel([x, y, z], float(value))
        
        return image
    
    def test_itk_to_pyvista_basic(self):
        """Test basic ITK to PyVista conversion."""
        image = self.create_test_itk_image()
        grid = itk_image_to_pyvista_grid(image)
        
        assert isinstance(grid, pv.UniformGrid)
        assert grid.dimensions == (10, 10, 10)
        assert np.allclose(grid.spacing, (1.0, 1.0, 1.0))
        assert np.allclose(grid.origin, (0.0, 0.0, 0.0))
        assert "scalars" in grid.point_data
    
    def test_itk_to_pyvista_custom_properties(self):
        """Test ITK to PyVista conversion with custom spacing and origin."""
        spacing = (0.5, 1.0, 2.0)
        origin = (10.0, 20.0, 30.0)
        image = self.create_test_itk_image(spacing=spacing, origin=origin)
        grid = itk_image_to_pyvista_grid(image)
        
        assert np.allclose(grid.spacing, spacing)
        assert np.allclose(grid.origin, origin)
    
    def test_pyvista_to_itk_basic(self):
        """Test basic PyVista to ITK conversion."""
        dims = (10, 10, 10)
        spacing = (1.0, 1.0, 1.0)
        origin = (0.0, 0.0, 0.0)
        
        grid = pv.UniformGrid(dims=dims, spacing=spacing, origin=origin)
        values = np.arange(np.prod(dims), dtype=np.float32)
        grid.point_data["scalars"] = values
        
        image = pyvista_grid_to_itk_image(grid)
        
        assert image.GetLargestPossibleRegion().GetSize() == list(dims)
        assert np.allclose(image.GetSpacing(), spacing)
        assert np.allclose(image.GetOrigin(), origin)
    
    def test_pyvista_to_itk_no_data(self):
        """Test PyVista to ITK conversion with no point data."""
        grid = pv.UniformGrid(dims=(10, 10, 10))
        
        with pytest.raises(ValueError, match="No point data arrays"):
            pyvista_grid_to_itk_image(grid)
    
    def test_pyvista_to_itk_wrong_type(self):
        """Test PyVista to ITK conversion with wrong grid type."""
        mesh = pv.PolyData()
        
        with pytest.raises(TypeError, match="Expected pv.UniformGrid"):
            pyvista_grid_to_itk_image(mesh)
    
    def test_round_trip_conversion(self):
        """Test round-trip conversion ITK -> PyVista -> ITK."""
        original_image = self.create_test_itk_image(
            size=(5, 6, 7),
            spacing=(0.5, 1.0, 1.5),
            origin=(10.0, 20.0, 30.0)
        )
        
        grid = itk_image_to_pyvista_grid(original_image)
        converted_image = pyvista_grid_to_itk_image(grid)
        
        assert converted_image.GetLargestPossibleRegion().GetSize() == [5, 6, 7]
        assert np.allclose(converted_image.GetSpacing(), (0.5, 1.0, 1.5))
        assert np.allclose(converted_image.GetOrigin(), (10.0, 20.0, 30.0))
        
        original_array = itk.GetArrayFromImage(original_image)
        converted_array = itk.GetArrayFromImage(converted_image)
        assert np.allclose(original_array, converted_array)
    
    def test_data_preservation(self):
        """Test that data values are preserved during conversion."""
        image = self.create_test_itk_image(size=(4, 4, 4))
        grid = itk_image_to_pyvista_grid(image)
        
        original_array = itk.GetArrayFromImage(image)
        grid_array = grid.point_data["scalars"].reshape(grid.dimensions[::-1])
        
        assert np.allclose(original_array, grid_array)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])