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
from matplotlib.ticker import ScalarFormatter


def plot_format_w_e(fig, ax, latitude, time, path):
    ax.invert_yaxis()
    plt.yscale('log')
    ax.set_yticks([1000, 800, 600, 400, 300, 200])
    ax.yaxis.set_major_formatter(ScalarFormatter())
    
    ax.set_title(f"west-east: lat = {latitude}, time = {str(time).split(':')[0]}")
    ax.set_ylabel("level [hpa]")
    ax.set_xlabel("longitude [°E]")
    fig.savefig(path, dpi=dpi)

def plot_vert_w_e_geopotential(latitude, time):
    """
     creates a figure and axis and plots geopotential lines on it

     Parameters
     ----------
     longitude : longitude of dataset
     time : current timestamp (dimension value of dataset)
     pot : bool for using potential temperature

     Returns
     -------
     fig : current figure handle
     ax : current axis handle

     """
    fig, ax = plt.subplots(figsize=(8, 7))

    c = ds.sel(latitude=latitude, time=time).z.plot.contour(ax= ax, colors='k', linewidths=0.7,
                                                      add_colorbar = False)
    ax.clabel(c, c.levels, inline=True, fmt=fmt, fontsize=12)

    return fig, ax

def plot_vertical_w_e_temp(latitude, time, path, pot):
    """
    plots the vertical west east temperature cut and the corresponding wind barbs

    Parameters
    ----------
    latitude : longitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : bool for using potential temperature

    Returns
    -------
    None

    """
    fig, ax = plot_vert_w_e_geopotential(latitude, time)
    if pot == True:
        mesh_t_pot = ds.sel(latitude=latitude, time=time).t_pot.plot.contourf(ax=ax, levels=contour_lvls, 
                                                                 cmap=cmap_temp, vmin=vmin_pot, 
                                                                 vmax=vmax_pot, add_colorbar = False)
        plt.colorbar(mesh_t_pot, ax=ax, label='pot temperature [K]')
    if pot == False:
        mesh_t = ds.sel(latitude=latitude, time=time).t_c.plot.contourf(ax=ax, levels=contour_lvls, 
                                                               cmap=cmap_temp, vmin=vmin_c, 
                                                               vmax=vmax_c, add_colorbar = False)
        plt.colorbar(mesh_t, ax=ax, label='temperature [°C]')

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

    plot_format_w_e(fig, ax, latitude, time, path) # add axis labels, change to log y axis & save plot
    plt.close()
    # plt.show()

def plot_vertical_w_e_hum(latitude, time, path):
    """
    plots the vertical west east temperature contour lines with relative humidity

    Parameters
    ----------
    latitude : longitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename

    Returns
    -------
    None

    """
    fig, ax = plot_vert_w_e_geopotential(latitude, time)
    # Apply the masks to the data variable
    masked_data = xr.where(ds['r'] > 90, 2, xr.where(ds['r'] > 75, 1, np.nan))

    # Create the contourf plot using xarray's plot function
    mesh = masked_data.sel(latitude=latitude, time=time).plot.contourf(levels=[0, 1, 2],
                                                                 colors=['#7EDF7F', '#249527'],
                                                                 add_colorbar=False,
                                                                 ax=ax)

    sp = surface_p.sel(latitude=latitude, time=time)
    sp = sp / 100
    sp = sp.where(sp['sp'] < 1000, 1000)
    ax.fill_between(sp.longitude, sp.sp, 1000, color='grey')

    cbar = plt.colorbar(mesh, ax=ax, shrink=0.5, label='relative Humidity [%]')
    cbar.set_ticks([0.5, 1.5])
    cbar.set_ticklabels(['> 75', '> 90'])

    

    plot_format_w_e(fig, ax, latitude, time, path)
    plt.close()
    # plt.show()

def plot_vertical_w_e_cc(latitude, time, path):
    """
    plots the vertical east west temperature contour lines and cloud cover

    Parameters
    ----------
    latitude : longitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename

    Returns
    -------
    None

    """
    fig, ax = plot_vert_w_e_geopotential(latitude, time)
    mesh_cc = ds.sel(latitude=latitude, time=time).cc.plot.contourf(ax=ax, cmap=cmap_cloud,
                                                                add_colorbar=False)

    sp = surface_p.sel(latitude=latitude, time=time)
    sp = sp / 100
    sp = sp.where(sp['sp'] < 1000, 1000)
    ax.fill_between(sp.longitude, sp.sp, 1000, color='grey')

    plt.colorbar(mesh_cc, ax=ax, label='cloud cover fraction [0-1]')
    
    plot_format_w_e(fig, ax, latitude, time, path)
    plt.close()
    # plt.show()
    
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
    
def myround(x, base=5):
    return base * round(x/base)


ds = xr.open_dataset(r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5_data_may_v4.nc')
surface_p = xr.open_dataset(r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\surface_p.nc')
ds = ds.assign(t_c = ds["t"] - 273.15)
ds = ds.assign(t_pot = ds["t"] * (1000 / ds.level) ** (2 / 7))

dpi = 200 # quality of saved png pics
lats = ds.latitude.values[::8]
times = ds.time.values
contour_lvls = 10
vmin_c = myround(np.min(ds.t_c.values)) # min temp [°C] for colormap
vmax_c = myround(np.max(ds.t_c.values))
vmin_pot = myround(np.min(ds.t_pot.values))
vmax_pot = myround(np.max(ds.t_pot.values))

cmap_cloud = plt.get_cmap('Blues', 6)
cmap_temp = plt.get_cmap('coolwarm', contour_lvls)

variables = ["temp", "pot_temp", "hum", "cc"]

for time in times:
    time_str = pd.Timestamp(time).strftime("%Y%m%d_%H") # convert time to str for saving
    if not os.path.exists("../era5vert_w_e/"):
        os.mkdir("../era5vert_w_e/")
    if not os.path.exists(f"../era5vert_w_e/{time_str}/"):
        os.mkdir(f"../era5vert_w_e/{time_str}/")

    current_dir = f"../era5vert_w_e/{time_str}/"
    
    for var in variables:
        for lat in lats:
            path_temp = current_dir + f'{time_str}_{lat}_vert_w_e_{var}.png'
            
            if os.path.exists(path_temp):
                continue
            if var == "temp":
                plot_vertical_w_e_temp(lat, time, path_temp, pot = False)
            elif var == "pot_temp":
                plot_vertical_w_e_temp(lat, time, path_temp, pot = True)
            elif var == "hum":
                plot_vertical_w_e_hum(lat, time, path_temp)
            elif var == "cc":
                plot_vertical_w_e_cc(lat, time, path_temp)
