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
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

def plot_format_n_s(fig, ax, longitude, time, path):
    """
    function for formatting the plots: title, axis labels & saving, ...

    Parameters
    ----------
    fig : 
    ax : 
    longitude : 
    time : 
    path : 

    Returns
    -------
    None.

    """
    
    ax.set_ylabel("level [hpa]")
    ax.set_title(f"north-south: lon = {longitude}, time = {str(time).split(':')[0]}")
    ax.invert_yaxis()
    plt.yscale('log')
    ax.set_yticks([1000, 800, 600, 400, 300, 200])
    ax.yaxis.set_major_formatter(ScalarFormatter())
    fig.savefig(path, dpi=dpi)

def plot_vert_n_s_geopotential(longitude, time):
    """
    creates a figure and axis and plots temperature contour lines on it

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
    c = ds.sel(longitude=longitude, time=time).z.plot.contour(ax= ax, colors='k', linewidths=0.7,
                                                      add_colorbar = False)
    ax.clabel(c, c.levels, inline=True, fmt=fmt, fontsize=12)

    return fig, ax

def plot_vertical_n_s_temp(longitude, time, path, pot):
    """
    plots the vertical north south temperature cut and the corresponding wind barbs

    Parameters
    ----------
    longitude : longitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : bool for using potential temperature

    Returns
    -------
    None

    """
    fig, ax = plot_vert_n_s_geopotential(longitude, time)
    if pot:
        mesh_t_pot = ds.sel(longitude=longitude, time=time).t_pot.plot.contourf(ax=ax, 
                                                                                levels=np.arange(vmin_pot,  vmax_pot, 5), 
                                                                                vmin = vmin_pot, vmax = vmax_pot, 
                                                                                cmap=cmap_temp, add_colorbar = False)
        plt.colorbar(mesh_t_pot, ax=ax, label='pot temperature [K]')
    elif ~pot:
        mesh_t = ds.sel(longitude=longitude, time=time).t_c.plot.contourf(ax=ax, levels=np.arange(vmin_c,  vmax_c, 5), 
                                                                 vmin = vmin_c, vmax = vmax_c,
                                                                 cmap=cmap_temp,
                                                                 add_colorbar = False)
        plt.colorbar(mesh_t, ax=ax, label='temperature [°C]')

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
    
    # plot windbarbs
    skip_lat = dict(latitude=slice(None, None, 10))
    ax.barbs(lat[skip_lat], lvl_up, v_up[skip_lat], w_up[skip_lat], length=4.5)
    ax.barbs(lat[skip_lat], lvl_down, v_down[skip_lat], w_down[skip_lat], length=4.5)
    ax.fill_between(sp.latitude, sp.sp, 1000, color='grey')

    plot_format_n_s(fig, ax, longitude, time, path)
    plt.close()
    #plt.show()
    return

def plot_vertical_n_s_hum(longitude, time, path):
    """
    plots the vertical north south temperature contour lines and relative humidity

    Parameters
    ----------
    longitude : longitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : bool for using potential temperature

    Returns
    -------
    None

    """
    fig, ax = plot_vert_n_s_geopotential(longitude, time)
    # Apply the masks to the data variable
    masked_data = xr.where(ds['r'] > 90, 2, xr.where(ds['r'] > 75, 1, np.nan))

    # Create the contourf plot using xarray's plot function
    mesh = masked_data.sel(longitude=longitude, time=time).plot.contourf(levels=[0, 1, 2],
                                                                 colors=['#7EDF7F', '#249527'],
                                                                 add_colorbar=False,
                                                                 ax=ax)

    sp = surface_p.sel(longitude=longitude, time=time)
    sp = sp / 100
    sp = sp.where(sp['sp'] < 1000, 1000)
    ax.fill_between(sp.latitude, sp.sp, 1000, color='grey')

    cbar = plt.colorbar(mesh, ax=ax, shrink=0.5, label='relative Humidity [%]')
    cbar.set_ticks([0.5, 1.5])
    cbar.set_ticklabels(['> 75', '> 90'])
    
    plot_format_n_s(fig, ax, longitude, time, path)
    plt.close()
    #plt.show()
    return

def plot_vertical_n_s_cc(longitude, time, path):
    """
    plots the vertical north south temperature contour lines and cloud cover

    Parameters
    ----------
    lon : longitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : bool for using potential temperature

    Returns
    -------
    None

    """
    fig, ax = plot_vert_n_s_geopotential(longitude, time)
    mesh_cc = ds.sel(longitude=longitude, time=time).cc.plot.contourf(ax= ax, cmap=cmap_cloud,
                                                       add_colorbar = False)
    # select the according topography for this cut 
    sp = surface_p.sel(longitude=longitude, time=time)
    sp = sp / 100 # transform to hpa
    sp = sp.where(sp['sp'] < 1000, 1000) # mask topography-points to 1000
    ax.fill_between(sp.latitude, sp.sp, 1000, color='grey') # fill with grey 

    plt.colorbar(mesh_cc, ax=ax, label='cloud cover fraction [0-1]')
    
    plot_format_n_s(fig, ax, longitude, time, path)
    plt.close()
    #plt.show()
    return

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

if __name__ == '__main__':
    # Load ERA5 data from NetCDF file
    ds = xr.open_dataset(r'C:\Users\dgratzl\OneDrive - Austro Control GmbH\era5_data_may_v3.nc')

    # load model topography in Pa
    surface_p = xr.open_dataset(r'C:\Users\dgratzl\OneDrive - Austro Control GmbH\ERA\surface_p.nc')
    ds = ds.assign(t_c = ds["t"] - 273.15)
    ds = ds.assign(t_pot = ds["t"] * (1000 / ds.level) ** (2 / 7))

    dpi = 200 # quality of saved png pics
    lons = ds.longitude.values[::8]
    times = ds.time.values
    contour_lvls = 10 # for temp
    vmin_c = myround(np.min(ds.t_c.values))
    vmax_c = myround(np.max(ds.t_c.values))
    vmin_pot = myround(np.min(ds.t_pot.values))
    vmax_pot = myround(np.max(ds.t_pot.values))

    cmap_cloud = plt.get_cmap('Blues', 6)
    cmap_temp = plt.get_cmap('coolwarm', contour_lvls)
    variables = ["temp", "pot_temp", "hum", "cc"]

    for time in times:
        time_str = pd.Timestamp(time).strftime("%Y%m%d_%H") # convert time to str for saving

        if not os.path.exists("../era5vert_n_s/"):
            os.mkdir("../era5vert_n_s/")
        if not os.path.exists(f"../era5vert_n_s/{time_str}/"):
            os.mkdir(f"../era5vert_n_s/{time_str}/")
        current_dir = f"../era5vert_n_s/{time_str}/"

        for var in variables:
            for lon in lons:
                path_temp = current_dir + f'{time_str}_{lon}_vert_n_s_{var}.png'
                
                if os.path.exists(path_temp):
                    continue
                if var == "temp":
                    plot_vertical_n_s_temp(lon, time, path_temp, pot = False)
                elif var == "pot_temp":
                    plot_vertical_n_s_temp(lon, time, path_temp, pot = True)
                elif var == "hum":
                    plot_vertical_n_s_hum(lon, time, path_temp)
                elif var == "cc":
                    plot_vertical_n_s_cc(lon, time, path_temp)