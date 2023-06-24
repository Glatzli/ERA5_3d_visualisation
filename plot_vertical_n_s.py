# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:06:50 2023

@author: Surface Pro
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load ERA5 data from NetCDF file
ds = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\era5_data_may.nc')
surface_p = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\surface_p.nc')

def plot_vert_n_s_geopotential(longitude, time):
    fig, ax = plt.subplots(figsize=(8, 7))
    ds.sel(longitude=longitude, time=time).t_c.plot.contour(ax=ax, colors='k')

    return fig, ax

def plot_vertical_n_s_temp(longitude, time, path):
    fig, ax = plot_vert_n_s_geopotential(lon, time)
    ds.sel(longitude=longitude, time=time).t_c.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

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

    skip = dict(latitude=slice(None,None,10))
    ax.barbs(lat[::10], lvl, v[skip], w[skip], length=5)

    lvl_up = lvl[skip_up]
    v_up = v[skip_up]
    w_up = w[skip_up]

    lvl_down = lvl[skip_down]
    v_down = v[skip_down]
    w_down = w[skip_down]

    skip_lat = dict(latitude=slice(None, None, 10))
    ax.barbs(lat[skip_lat], lvl_up, v_up[skip_lat], w_up[skip_lat], length=5)
    ax.barbs(lat[skip_lat], lvl_down, v_down[skip_lat], w_down[skip_lat], length=5)
    ax.fill_between(sp.latitude, sp.sp, 1000, color='grey')

    ax.invert_yaxis()
    plt.yscale('log')
    fig.savefig(path, dpi=dpi)
    plt.close()
    #plt.show()

def plot_vertical_n_s_hum(longitude, time, path):
    fig, ax = plot_vert_n_s_geopotential(lon, time)
    # Apply the masks to the data variable
    masked_data = xr.where(ds['r'] > 90, 2, xr.where(ds['r'] > 75, 1, np.nan))

    # Create the contourf plot using xarray's plot function
    mesh = masked_data.sel(longitude=longitude, time=time).plot.contourf(levels=[0, 1, 2],
                                                                 colors=['#7EDF7F', '#249527'],
                                                                 add_colorbar=False,
                                                                 ax=ax)
    cbar = plt.colorbar(mesh, ax=ax, shrink=0.5, label='relative Humidity [%]')
    cbar.set_ticks([0.5, 1.5])
    cbar.set_ticklabels(['> 75', '> 90'])
    ax.set_title(f"lon = {longitude}, time = {str(time).split(':')[0]}")

    plt.yscale('log')
    fig.savefig(path, dpi=dpi)
    plt.close()
    #plt.show()

def plot_vertical_n_s_cc(lon, time, path):
    fig, ax = plot_vert_n_s_geopotential(lon, time)
    mesh_cc = ds.sel(longitude=lon, time=time).cc.plot.contourf(ax= ax, cmap=cmap_cloud,
                                                       add_colorbar = False)
    plt.colorbar(mesh_cc, ax=ax, label='cloud cover fraction [0-1]')
    ax.set_title(f"lon = {lon}, time = {str(time).split(':')[0]}")
    ax.invert_yaxis()
    plt.yscale('log')
    fig.savefig(path, dpi=dpi)
    plt.close()
    #plt.show()

# Load ERA5 data from NetCDF file
ds = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\era5_data_may.nc')
surface_p = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\surface_p.nc')
ds = ds.assign(t_c = ds["t"] - 273.15)

dpi = 100 # quality of saved png pics
lons = ds.longitude.values[::8]
times = ds.time.values

cmap_cloud = plt.get_cmap('Blues', 6)

variables = ["temp, hum, cc"]


for time in times:
    time_str = pd.Timestamp(time).strftime("%Y%m%d_%H") # convert time to str for saving

    if not os.path.exists("../era5vert_n_s/"):
        os.mkdir("../era5vert_n_s/")
    if not os.path.exists(f"../era5vert_n_s/{time_str}/"):
        os.mkdir(f"../era5vert_n_s/{time_str}/")
    current_dir = f"../era5vert_n_s/{time_str}/"

    #for var in variables:
  #      for lon in lons:
   #         path_temp = current_dir + f'{time_str}_{lon}_vert_n_s_{var}.png'
    #        if os.path.exists(path_temp):
     #           continue

      #      if var == "temp":
      #          plot_vertical_n_s_temp(lon, time, path_temp)
      #      elif var == "hum":
      #          plot_vertical_n_s_hum(lon, time, path_hum)
      #      elif var == "cc":
      #          plot_vertical_n_s_cc(lon, time, path_cc)

    for lon in lons:
        path_temp = current_dir + f'{time_str}_{lon}_vert_n_s_temp.png'
        if os.path.exists(path_temp):
            continue

        plot_vertical_n_s_temp(lon, time, path_temp)

    for lon in lons:
        path_hum = current_dir + f'{time_str}_{lon}_vert_n_s_hum.png'
        if os.path.exists(path_hum):
            continue

        plot_vertical_n_s_hum(lon, time, path_hum)

    for lon in lons:
        path_cc = current_dir + f'{time_str}_{lon}_vert_n_s_cc.png'
        if os.path.exists(path_cc):
            continue

        plot_vertical_n_s_cc(lon, time, path_cc)


