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

def plot_vertical_ns(longitude, time):

    # Create a horizontal
    fig, ax = plt.subplots(figsize=(8, 6))

    ds.sel(longitude=longitude, time=time).t.plot.contour(ax=ax, colors='k')
    ds.sel(longitude=longitude, time=time).t.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

    lat = ds.sel(longitude=longitude, time=time).latitude
    lvl = ds.sel(longitude=longitude, time=time).level
    v = ds.sel(longitude=longitude, time=time).v
    omega = ds.sel(longitude=longitude, time=time).w
    sp = surface_p.sel(longitude=longitude, time=time)


    R = 287.05
    rho = lvl / (R*ds.sel(longitude=longitude, time=time).t)
    w = - (omega/rho)
    sp = sp/100
    sp = sp.where(sp['sp'] < 1000, 1000)

    skip_up = dict(level=slice(None, 11, None))
    skip_down = dict(level=slice(12, None, 3))

    lvl_up = lvl[skip_up]
    v_up = v[skip_up]
    w_up = w[skip_up]

    lvl_down = lvl[skip_down]
    v_down = v[skip_down]
    w_down = w[skip_down]

    skip_lat = dict(latitude=slice(None, None, 10))
    ax.barbs(lat[skip_lat], lvl_up, v_up[skip_lat], w_up[skip_lat], length=5)
    ax.barbs(lat[skip_lat], lvl_down, v_down[skip_lat], w_down[skip_lat], length=5)
    ax.fill_between(sp.latitude, sp.sp, 1000, color = 'grey')

    ax.invert_yaxis()

    plt.yscale('log')
    plt.show()

lon = 10
t = '2023-05-08T00-00-00'

plot_vertical_ns(lon, t)