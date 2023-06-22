# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:06:50 2023

@author: Surface Pro
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import pandas as pd

def plot_vertical_ns_temp(longitude, time, path):

    # Create a horizontal
    fig, ax = plt.subplots(figsize=(8, 6))

    ds.sel(longitude=longitude, time=time).t_c.plot.contour(ax=ax, colors='k')
    ds.sel(longitude=longitude, time=time).t_c.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

    lat = ds.sel(longitude=longitude, time=time).latitude
    lvl = ds.sel(longitude=longitude, time=time).level
    v = ds.sel(longitude=longitude, time=time).v
    omega = ds.sel(longitude=longitude, time=time).w


    R = 287.05
    rho = lvl / (R*ds.sel(longitude=longitude, time=time).t)
    w = - (omega/rho)

    skip = dict(latitude=slice(None,None,10))
    ax.barbs(lat[::10], lvl, v[skip], w[skip], length=5)


    ax.invert_yaxis()

    plt.yscale('log')
    fig.savefig(path, dpi=400)
    plt.close()

# Load ERA5 data from NetCDF file
ds = xr.open_dataset(
    r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5_data_may_v2.nc')
ds = ds.assign(t_c = ds["t"] - 273.15)

lons = ds.longitude.values[0::8]
times = ds.time.values[0:5]

for time in times:
    time_str = pd.Timestamp(time).strftime("%Y%m%d_%H") # convert time to str for saving
    
    if not os.path.exists("../era5vert_n_s/"):
        os.mkdir("../era5vert_n_s/") 
    if not os.path.exists(f"../era5vert_n_s/{time_str}/"):
        os.mkdir(f"../era5vert_n_s/{time_str}/")
    current_dir = f"../era5vert_n_s/{time_str}/"    
    
    for lon in lons:
        path_temp = current_dir + f'{time_str}_{lon}_vert_n_s_temp.png'
        if os.path.exists(path_temp):
            continue
        plot_vertical_ns_temp(lon, time, path_temp)
        

