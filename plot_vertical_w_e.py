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


def plot_vert_w_e_temp_lines(latitude, time, pot):
    fig, ax = plt.subplots(figsize=(8, 7))
    if pot == True:
        ds.sel(latitude=latitude, time=time).t_pot.plot.contour(ax=ax, levels=contour_lvls, colors='k')
    if pot == False:
        ds.sel(latitude=latitude, time=time).t_c.plot.contour(ax=ax, levels=contour_lvls, colors='k')
    return fig, ax

def plot_vertical_w_e_temp(latitude, time, path, pot):
    fig, ax = plot_vert_w_e_temp_lines(latitude, time, pot)
    if pot == True:
        ds.sel(latitude=latitude, time=time).t_pot.plot.contourf(ax=ax, levels=contour_lvls, cmap='coolwarm')
    if pot == False:
        ds.sel(latitude=latitude, time=time).t_c.plot.contourf(ax=ax, levels=contour_lvls, cmap='coolwarm')

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
    # plt.show()

def plot_vertical_w_e_hum(latitude, time, path):
    fig, ax = plot_vert_w_e_temp_lines(latitude, time, False)
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

def plot_vertical_w_e_cc(lon, time, path):
    fig, ax = plot_vert_w_e_temp_lines(lon, time, False)
    mesh_cc = ds.sel(latitude=lat, time=time).cc.plot.contourf(ax=ax, cmap=cmap_cloud,
                                                                add_colorbar=False)
    plt.colorbar(mesh_cc, ax=ax, label='cloud cover fraction [0-1]')
    ax.set_title(f"lon = {lon}, time = {str(time).split(':')[0]}")
    ax.invert_yaxis()
    plt.yscale('log')
    fig.savefig(path, dpi=dpi)
    plt.close()
    # plt.show()


ds = xr.open_dataset(
    r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5_data_may_v4.nc')
surface_p = xr.open_dataset(
    r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\surface_p.nc')
ds = ds.assign(t_c = ds["t"] - 273.15)
ds = ds.assign(t_pot = ds["t"] * (1013 / ds.level) ** (2 / 7))

dpi = 100 # quality of saved png pics
lats = ds.latitude.values[::8]
times = ds.time.values
contour_lvls = 10

cmap_cloud = plt.get_cmap('Blues', 6)

#variables = ["temp", "pot_temp", "hum", "cc"]

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
        plot_vertical_w_e_temp(lat, time, path_temp, pot = False)

    for lat in lats:
        path_temp = current_dir + f'{time_str}_{lat}_vert_w_e_pot_temp.png'
        if os.path.exists(path_temp):
            continue
        plot_vertical_w_e_temp(lat, time, path_temp, pot = True)

    for lat in lats:
        path_hum = current_dir + f'{time_str}_{lat}_vert_w_e_hum.png'
        if os.path.exists(path_hum):
            continue

        plot_vertical_w_e_hum(lat, time, path_hum)

    for lat in lats:
        path_cc = current_dir + f'{time_str}_{lat}_vert_n_s_cc.png'
        if os.path.exists(path_cc):
            continue

        plot_vertical_w_e_cc(lat, time, path_cc)

