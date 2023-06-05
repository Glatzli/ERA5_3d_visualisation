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

def plot_vertical_ns(longitude, time):

    # Create a horizontal
    fig, ax = plt.subplots(figsize=(8, 6))

    ds.sel(longitude=longitude, time=time).t.plot.contour(ax=ax, colors='k')
    ds.sel(longitude=longitude, time=time).t.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

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
    plt.show()

lat = 10
t = '2023-05-08T00-00-00'

plot_vertical_ns(lat, t)