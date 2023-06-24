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


def plot_vert_w_e_geopotential(latitude, time):
    fig, ax = plt.subplots(figsize=(8, 7))
    ds.sel(latitude=latitude, time=time).t_c.plot.contour(ax=ax, colors='k')

    return fig, ax

def plot_vertical_we_temp(latitude, time, path):
    fig, ax = plot_vert_w_e_geopotential(latitude, time)
    ds.sel(latitude=latitude, time=time).t_c.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

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
    fig.savefig(path, dpi=dpi)
    plt.close()


def plot_vertical_w_e_hum(latitude, time, path):
    fig, ax = plot_vert_w_e_geopotential(latitude, time)
    # Apply the masks to the data variable
    masked_data = xr.where(ds['r'] > 90, 2, xr.where(ds['r'] > 75, 1, np.nan))

    # Create the contourf plot using xarray's plot function
    mesh = masked_data.sel(latitude=latitude, time=time).plot.contourf(levels=[0, 1, 2],
                                                                 colors=['#7EDF7F', '#249527'],
                                                                 add_colorbar=False,
                                                                 ax=ax)
    cbar = plt.colorbar(mesh, ax=ax, shrink=0.5, label='relative Humidity [%]')
    cbar.set_ticks([0.5, 1.5])
    cbar.set_ticklabels(['> 75', '> 90'])
    ax.set_title(f"lat = {latitude}, time = {str(time).split(':')[0]}")

    ax.invert_yaxis()

    plt.yscale('log')
    fig.savefig(path, dpi=dpi)
    plt.close()
    #plt.show()


ds = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\era5_data_may.nc')
surface_p = xr.open_dataset(
    r'C:\Users\Timm\PycharmProjects\SciProg\era5-3d-visualisation\surface_p.nc')
ds = ds.assign(t_c = ds["t"] - 273.15)

dpi = 100 # quality of saved png pics
lats = ds.latitude.values[::8]
times = ds.time.values

for time in times:
    time_str = pd.Timestamp(time).strftime("%Y%m%d_%H") # convert time to str for saving
    if not os.path.exists("../era5vert_w_e/"):
        os.mkdir("../era5vert_w_e/")
    if not os.path.exists(f"../era5vert_w_e/{time_str}/"):
        os.mkdir(f"../era5vert_w_e/{time_str}/")

    current_dir = f"../era5vert_w_e/{time_str}/"

    for lat in lats:
        path_temp = current_dir + f'{time_str}_{lat}_vert_w_e_temp.png'
        if os.path.exists(path_temp):
            continue
        plot_vertical_we_temp(lat, time, path_temp)

    for lat in lats:
        path_hum = current_dir + f'{time_str}_{lat}_vert_w_e_hum.png'
        if os.path.exists(path_hum):
            continue

        plot_vertical_w_e_hum(lat, time, path_hum)

