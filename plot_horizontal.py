import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

def plot_horizontal(level, time):
    
    if level <= 300: # set min/maxs of colormap according to pressure level
        vmax = -25; vmin = -85
    elif level <= 500:
        vmax = 10; vmin = -50
    elif level <= 700:
        vmax = 25; vmin = -35
    elif level <= 800:
        vmax = 30; vmin = -30
    elif level <= 850:
        vmax = 35; vmin = -25
    elif level <= 925:
        vmax = 40; vmin = -20
    else:
        vmax = 45; vmin = -15
    
    # Create a horizontal
    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.NaturalEarthFeature( 
        category='cultural',
        name='admin_0_countries',
        scale='50m',
        facecolor='none',
        edgecolor='black',
        linewidth = 0.2
    ))
    ax.set_extent([-4, 26, 31, 60])
    
    cmap=plt.get_cmap('RdBu_r', 14)
    
    c = ds.sel(level=level, time=time).z.plot.contour(ax= ax, colors='k', linewidths=0.7)
    ax.clabel(c, c.levels, inline=True, fmt=fmt, fontsize=8)
    ds.sel(level=level, time=time).t_c.plot.contourf(ax= ax, levels=np.arange(vmin,  vmax, 5), cmap=cmap, vmin=vmin, vmax=vmax)
    
    return fig, ax

def fmt(x):
    """
    formats the labels of geopotential height to 10m

    Parameters
    ----------
    x : geopotential height [dm] as float

    Returns
    -------
    s : geopotential height [10m] as str w/o trailing zeros

    """
    x = x / 100
    s = f"{x:.0f}"
    return s
    

# Load ERA5 data from NetCDF file
ds = xr.open_dataset(r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5_data_may_v2.nc')
ds = ds.assign(t_c = ds["t"] - 273.15)

levels = ds.level.values # hpa 100, 200, 300, 400, 500, 600, 700,
times = ds.time.values[0:2]# '2023-04-22T00-00-00' #timestamp

for level in levels:
    for time in times:
        fig, ax = plot_horizontal(level, time)
        #plt.show()
        
        # save fig to specific dir
        #my_path = os.path.abspath(__file__) # get current path
        time_str = pd.Timestamp(time).strftime("%Y%m%d_%H") # convert time to str for saving
        my_file = f'../era5horiz_plots/{time_str}_{level}_era5_horiz.png'
        
        fig.savefig(my_file, dpi=400)
