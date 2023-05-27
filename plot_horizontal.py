import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

# Load ERA5 data from NetCDF file
ds = xr.open_dataset(r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5_data_april_v1.nc')

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
    
    # search for level&time value in dataset
    
    ds.sel(level=level, time=time).z.plot.contour(ax= ax, colors='k')
    ds.sel(level=level, time=time).t.plot.contourf(ax= ax, levels=10, cmap='coolwarm')

    return fig, ax

levels = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000] # hpa
time = '2023-04-22T00-00-00' #timestamp

for level in levels:
    fig, ax = plot_horizontal(level, time)
    plt.show()
    
    # save fig to specific dir
    #my_path = os.path.abspath(__file__) # get current path
    my_file = f'../era5horiz_plots/{time}_{level}_era5_horiz.png'
    
    fig.savefig(my_file, dpi=400)
