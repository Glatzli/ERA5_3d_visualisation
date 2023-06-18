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
surface_p = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\surface_p.nc')

def plot_vertical_we(latitude, time):

    # Create a horizontal
    fig, ax = plt.subplots(figsize=(8, 6))

    ds.sel(latitude=latitude, time=time).t.plot.contour(ax=ax, colors='k')
    ds.sel(latitude=latitude, time=time).t.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

    lon = ds.sel(latitude=latitude, time=time).longitude
    lvl = ds.sel(latitude=latitude, time=time).level
    u = ds.sel(latitude=latitude, time=time).u
    omega = ds.sel(latitude=latitude, time=time).w
    sp = surface_p.sel(latitude=latitude, time=time)


    R = 287.05
    rho = lvl / (R*ds.sel(latitude=latitude, time=time).t)
    w = - (omega/rho)
    sp = sp/100
    sp = sp.where(sp['sp'] < 1000, 1000)

    skip_up = dict(level=slice(None,11,None))
    skip_down = dict(level=slice(12, None, 3))

    lvl_up = lvl[skip_up]
    u_up = u[skip_up]
    w_up = w[skip_up]

    lvl_down = lvl[skip_down]
    u_down = u[skip_down]
    w_down = w[skip_down]

    skip_lon = dict(longitude=slice(None,None,10))
    ax.barbs(lon[skip_lon], lvl_up, u_up[skip_lon], w_up[skip_lon], length=5)
    ax.barbs(lon[skip_lon], lvl_down, u_down[skip_lon], w_down[skip_lon], length=5)
    ax.fill_between(sp.longitude, sp.sp, 1000, color = 'grey')

    ax.invert_yaxis()

    plt.yscale('log')
    plt.show()

lat = 40
t = '2023-05-08T00-00-00'
plot_vertical_we(lat, t)