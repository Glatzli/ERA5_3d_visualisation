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

# Load ERA5 data from NetCDF file
ds = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\era5_data_may.nc')

def plot_vertical_we(latitude, time):

    # Create a horizontal
    fig, ax = plt.subplots(figsize=(8, 6))

    ds.sel(latitude=latitude, time=time).t.plot.contour(ax=ax, colors='k')
    ds.sel(latitude=latitude, time=time).t.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

    lon = ds.sel(latitude=latitude, time=time).longitude
    lvl = ds.sel(latitude=latitude, time=time).level
    u = ds.sel(latitude=latitude, time=time).u
    omega = ds.sel(latitude=latitude, time=time).w


    R = 287.05
    rho = lvl / (R*ds.sel(latitude=latitude, time=time).t)
    w = - (omega/rho)

    skip = dict(longitude=slice(None,None,10))
    ax.barbs(lon[::10], lvl, u[skip], w[skip], length=5)


    ax.invert_yaxis()

    plt.yscale('log')
    plt.show()

lon = 40
t = '2023-05-08T00-00-00'
plot_vertical_we(lon, t)
