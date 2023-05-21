import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load ERA5 data from NetCDF file
ds = xr.open_dataset(r'C:\Users\Timm\Desktop\Atmospheric Sciences\Semester 2\Advanced Programming\era5_data_april_v1.nc')

def plot_horizontal(level, time):
    # Create a horizontal
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='50m',
        facecolor='none',
        edgecolor='black'
    ))
    ax.set_extent([-4, 26, 31, 60])
    ds.isel(level=level, time=time).z.plot.contour(ax= ax, colors='k')
    ds.isel(level=level, time=time).t.plot.contourf(ax= ax, levels=10, cmap='coolwarm')

    return fig, ax
fig, ax = plot_horizontal(5,5)
plt.show()