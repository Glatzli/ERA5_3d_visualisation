"""
    ERA5 project: try to merge all plotting functions to minimize lines;
    in 1 program
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib.ticker import ScalarFormatter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path


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

def create_fig_national_boundaries():
    """
    create a figure with national boundaries of central europe for horizontal plot

    Returns
    -------
    fig : figure handle
    ax : axis handle
    """
    fig = plt.figure(figsize=(8, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    gl = ax.add_feature(cfeature.NaturalEarthFeature( 
        category='cultural',
        name='admin_0_countries',
        scale='50m',
        facecolor='none',
        edgecolor='black',
        linewidth = 0.2
    ))
    
    ax.text(-0.1, 0.5, 'latitude', va='bottom', ha='center',
            rotation='vertical', rotation_mode='anchor',
            transform=ax.transAxes)
    ax.text(0.5, -0.1, 'longitude', va='bottom', ha='center',
            rotation='horizontal', rotation_mode='anchor',
            transform=ax.transAxes)
    
    gl = ax.gridlines(crs = ccrs.PlateCarree(), linewidth=0.5, draw_labels=True, 
                      linestyle='dashed', color='gray', alpha=0.5)
    
    gl.right_labels = False; gl.top_labels = False
    ax.set_extent([-4, 26, 31, 60])
    
    return fig, ax

def plot_horizontal_geopotential(ds, level, time, fig, ax):
    """
    plots geopotential as contour plot in an already existing figure

    Parameters
    ----------
    level : height level [hpa]
    time : current timestamp (dimension value of dataset)
    fig : current figure handle
    ax : current axis handle

    Returns
    -------
    fig : current figure handle
    ax : current axis handle

    """
    c = ds.sel(level=level, time=time).z.plot.contour(ax= ax, colors='k', linewidths=0.7,
                                                      add_colorbar = False)
    ax.clabel(c, c.levels, inline=True, fmt=fmt, fontsize=8)
    
    return fig, ax


def create_title(ax, param, time, view):
    """
    adds title for plots
    """
    match view:
        case "horiz":
            ax.set_title(f"level = {param}, time = {str(time).split(':')[0]}")
        case "vert_w_e":
            ax.set_title(f"west-east: lat = {param}, time = {str(time).split(':')[0]}")
        case "vert_n_s":
            ax.set_title(f"north-south: lon = {param}, time = {str(time).split(':')[0]}")
    

def plot_horizontal_temp(ds, level, time, path, vmin, vmax, cmap, contour_lvls_temp, dpi):
    fig, ax = create_fig_national_boundaries()
    fig, ax = plot_horizontal_geopotential(ds, level, time, fig, ax)
    mesh_t = ds.sel(level=level, time=time).t_c.plot.contourf(ax= ax, levels=np.arange(vmin,  vmax, contour_lvls_temp), 
                                                    cmap=cmap, vmin=vmin, vmax=vmax,
                                                    add_colorbar = False)
    plt.colorbar(mesh_t, ax=ax, label='temperature [°C]')
    create_title(ax, param=level, time=time, view="horiz")
    fig.savefig(path, dpi=dpi)
    plt.close()


def plot_horizontal_pot_temp(ds, level, time, path, vmin, vmax, cmap, contour_lvls_temp = 10, dpi=200):
    """
    plot geopotential and pot temp and save it

    Parameters
    ----------
    level : height level [hpa]
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename

    Returns
    -------
    None.

    """
    fig, ax = create_fig_national_boundaries()
    fig, ax = plot_horizontal_geopotential(ds, level, time, fig, ax)
       
    mesh_t = ds.sel(level=level, time=time).t_pot.plot.contourf(ax= ax, cmap=cmap, 
                                                                levels=np.arange(vmin,  vmax, contour_lvls_temp),
                                                                vmin = vmin, vmax = vmax,
                                                                add_colorbar = False)

    plt.colorbar(mesh_t, ax=ax, label='pot temperature [K]')
    create_title(ax, param=level, time=time , view="horiz")
    fig.savefig(path, dpi=dpi)
    plt.close()


def plot_horizontal_equiv_pot_temp(ds,*, level, time, path, vmin, vmax, cmap, contour_lvls_temp = 10, dpi=200):
    """
    plot equivalent pot temp with geopotential and plot it

    Parameters
    ----------
    level : height level [hpa]
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename

    Returns
    -------
    None.

    """
    fig, ax = create_fig_national_boundaries()
    fig, ax = plot_horizontal_geopotential(ds, level, time, fig, ax)
       
    mesh_t = ds.sel(level=level, time=time).eqpt.plot.contourf(ax= ax, cmap=cmap, 
                                                                levels=np.arange(vmin,  vmax, contour_lvls_temp),
                                                                vmin = vmin, vmax = vmax,
                                                                add_colorbar = False)

    plt.colorbar(mesh_t, ax=ax, label='equivalent pot temperature [K]')
    create_title(ax, param=level, time=time , view="horiz")
    fig.savefig(path, dpi=dpi)
    plt.close()


def mask_hum(ds):
    # Apply the masks to the data variable
    return xr.where(ds['r'] > 90, 2, xr.where(ds['r'] > 75, 1, np.nan))


def create_cbar_hum(ax, mesh):
    """
    create the colorbar for humidity plots
    """
    cbar = plt.colorbar(mesh, ax=ax, shrink=0.5, label='relative Humidity [%]')
    return cbar


def set_ticks_hum(cbar):
    """
    set ticks&ticklabels for humidity charts
    """
    cbar.set_ticks([0.5, 1.5])
    cbar.set_ticklabels(['> 75', '> 90'])

def plot_horizontal_hum(ds, *, masked_data, level, time, path, dpi=200, colors=['#7EDF7F', '#249527']):
    """
    plot humidity&geopotential and save it

    Parameters
    ----------
    level : height level [hpa]
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename

    Returns
    -------
    None.

    """
    fig, ax = create_fig_national_boundaries()
    fig, ax = plot_horizontal_geopotential(ds, level, time, fig, ax)    
    # masked_data = xr.where(ds['r'] > 90, 2, xr.where(ds['r'] > 75, 1, np.nan))
    # masked_data = mask_hum(ds)
    # Create the contourf plot using xarray's plot function
    mesh = masked_data.sel(level=level, time=time).plot.contourf(levels=[0, 1, 2], 
                                                                 colors=colors, 
                                                                 add_colorbar=False, 
                                                                 ax=ax)
    cbar = create_cbar_hum(ax, mesh)
    set_ticks_hum(cbar)
    create_title(ax, param=level, time=time, view="horiz")
    fig.savefig(path, dpi=dpi)
    plt.close()


def plot_horizontal_cc(ds, level, time, path, cmap_cloud, dpi=200):  
    """
    create cloud coverage plot and save it 

    Parameters
    ----------
    level : height level [hpa]
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename

    Returns
    -------
    None.

    """
    fig, ax = create_fig_national_boundaries()
    fig, ax = plot_horizontal_geopotential(ds, level, time, fig, ax)
    mesh_cc = ds.sel(level=level, time=time).cc.plot.contourf(ax= ax, cmap=cmap_cloud, 
                                                       add_colorbar = False)
    plt.colorbar(mesh_cc, ax=ax, label='cloud cover fraction [0-1]')
    create_title(ax, param=level, time=time, view="horiz")
    fig.savefig(path, dpi=dpi)
    plt.close()
    #plt.show()


# --------- vertical cut plotting functions
def plot_vert_geopotential(ds, *, latlon, time, view):
    """
     creates a figure and axis and plots geopotential lines on it

     Parameters
     ----------
     lat : longitude of dataset
     time : current timestamp (dimension value of dataset)
     pot : bool for using potential temperature

     Returns
     -------
     fig : current figure handle
     ax : current axis handle

     """
    fig, ax = plt.subplots(figsize=(8, 7))
    match view:
        case "vert_w_e":
            c = ds.sel(latitude=latlon, time=time).z.plot.contour(ax= ax, colors='k', linewidths=0.7, add_colorbar = False)
        case "vert_n_s":
            c = ds.sel(longitude=latlon, time=time).z.plot.contour(ax= ax, colors='k', linewidths=0.7,
                                                            add_colorbar = False)
    ax.clabel(c, c.levels, inline=True, fmt=fmt, fontsize=12)
    return fig, ax


def format_vert_plot(ax):
    """
    inverts y axis for pressure levels, change y axis to logarithmic and set tick labels
    """
    ax.invert_yaxis()
    plt.yscale('log')
    ax.set_yticks([1000, 800, 600, 400, 300, 200])
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.set_ylabel("level [hpa]")


def add_windbarbs(ds, latlon, time, ax, view): 
    """
    calculates the wind in the cross section and add it to current axis, selects only the needed windbarbs which should be plotted
    """
    length_barbs = 6
    # slice in vertical: till 11th level take every 3rd barb (from 200hpa on down), below only every 4th barb till ground level
    wind_slc_vert = list(range(0, 12, 3)) + list(range(12, 24, 4)) 
    wind_slc_horz = slice(None, None, 15)  # slice horizontally: only every 15th barb 
    if view == "vert_w_e":
        ds_slice_lat_time = ds.sel(latitude=latlon, time=time)  # 
        ax.barbs(ds_slice_lat_time.longitude[wind_slc_horz], ds_slice_lat_time.level[wind_slc_vert], 
                 ds_slice_lat_time.u_kt[wind_slc_vert, wind_slc_horz], 
                 ds_slice_lat_time.w_kt[wind_slc_vert, wind_slc_horz], length=length_barbs)

    elif view == "vert_n_s":
        ds_slice_lon_time = ds.sel(longitude=latlon, time=time)
        ax.barbs(ds_slice_lon_time.latitude[wind_slc_horz], ds_slice_lon_time.level[wind_slc_vert], 
                 ds_slice_lon_time.v_kt[wind_slc_vert, wind_slc_horz], 
                 ds_slice_lon_time.w_kt[wind_slc_vert, wind_slc_horz], length=length_barbs)
    return ax

def add_topography(surface_p, latlon, time, ax, view):
    """
    adds topography to the current axis, masks data and sets pixels to a grey color
    """
    if view == "vert_w_e":
        sp = surface_p.sel(latitude=latlon, time=time)
        sp_latlon = sp.longitude

    elif view == "vert_n_s":
        sp = surface_p.sel(longitude=latlon, time=time)
        sp_latlon = sp.latitude
    sp = sp/100
    sp = sp.where(sp['sp'] < 1000, 1000)
    ax.fill_between(sp_latlon, sp.sp, 1000, color = 'grey')
    return ax


def plot_vertical_temp(ds, *, surface_p, latlon, time, path_temp, vmin, vmax, cmap, contour_lvls_temp, view, dpi=200):
    """
    plots the vertical west east temperature [°C] cut with the corresponding wind barbs in that plane

    Parameters
    ----------
    lat: latitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : bool for using potential temperature

    Returns
    -------
    None

    """
    fig, ax = plot_vert_geopotential(ds, latlon=latlon, time=time, view=view)
    match view:
        case "vert_w_e":
            mesh_t = ds.sel(latitude=latlon, time=time).t_c.plot.contourf(ax=ax, levels=np.arange(vmin,  vmax, contour_lvls_temp), 
                                                                    cmap=cmap, vmin=vmin, 
                                                                    vmax=vmax, add_colorbar = False)
            ax.set_xlabel("longitude [°E]")
        case "vert_n_s":
            mesh_t = ds.sel(longitude=latlon, time=time).t_c.plot.contourf(ax=ax, levels=contour_lvls_temp, 
                                                                    cmap=cmap, vmin=vmin, 
                                                                    vmax=vmax, add_colorbar = False)
            ax.set_xlabel("latitude [°N]")
    plt.colorbar(mesh_t, ax=ax, label='temperature [°C]')
    ax = add_windbarbs(ds, latlon, time, ax, view)
    ax = add_topography(surface_p, latlon, time, ax, view)

    format_vert_plot(ax)
    create_title(ax, latlon, time, view)
    
    fig.savefig(path_temp, dpi=dpi)
    plt.close()
    # plt.show()


def plot_vertical_pot_temp(ds, *, surface_p, latlon, time, path_temp, vmin, vmax, cmap, contour_lvls_temp, view, dpi=200):
    """
    plots the vertical west east temperature [°C] cut with the corresponding wind barbs in that plane

    Parameters
    ----------
    lat: latitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : bool for using potential temperature

    Returns
    -------
    None

    """
    fig, ax = plot_vert_geopotential(ds, latlon=latlon, time=time, view=view)
    match view:
        case "vert_w_e":
            mesh_t_pot = ds.sel(latitude=latlon, time=time).t_pot.plot.contourf(ax=ax, levels=np.arange(vmin,  vmax, contour_lvls_temp), 
                                                                            cmap=cmap, vmin=vmin, 
                                                                            vmax=vmax, add_colorbar = False)
            ax.set_xlabel("longitude [°E]")
        case "vert_n_s":
            mesh_t_pot = ds.sel(longitude=latlon, time=time).t_pot.plot.contourf(ax=ax, levels=np.arange(vmin,  vmax, contour_lvls_temp), 
                                                                            cmap=cmap, vmin=vmin, 
                                                                            vmax=vmax, add_colorbar = False)
            ax.set_xlabel("latiude [°N]")
            
    plt.colorbar(mesh_t_pot, ax=ax, label='pot temperature [K]')
    ax = add_windbarbs(ds, latlon, time, ax, view)
    ax = add_topography(surface_p, latlon, time, ax, view)

    format_vert_plot(ax)
    create_title(ax, latlon, time, view)
    
    fig.savefig(path_temp, dpi=dpi)
    plt.close()
    # plt.show()


def plot_vertical_equiv_pot_temp(ds, *, surface_p, latlon, time, path_temp, vmin, vmax, cmap, contour_lvls_temp, view, dpi=200):
    """
    plots the vertical west east equiv pot temp cut; produces some nan data...

    Parameters
    ----------
    lat: latitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : bool for using potential temperature

    Returns
    -------
    None

    """
    fig, ax = plot_vert_geopotential(ds, latlon=latlon, time=time, view=view)
    match view:
        case "vert_w_e":
            mesh_t_pot = ds.sel(latitude=latlon, time=time).eqpt.plot.contourf(ax=ax, levels=np.arange(vmin,  vmax, contour_lvls_temp), 
                                                                            cmap=cmap, vmin=vmin, 
                                                                            vmax=vmax, add_colorbar = False)
            ax.set_xlabel("longitude [°E]")
        case "vert_n_s":
            mesh_t_pot = ds.sel(longitude=latlon, time=time).eqpt.plot.contourf(ax=ax, levels=np.arange(vmin,  vmax, contour_lvls_temp), 
                                                                            cmap=cmap, vmin=vmin, 
                                                                            vmax=vmax, add_colorbar = False)
            ax.set_xlabel("latiude [°N]")
            
    plt.colorbar(mesh_t_pot, ax=ax, label='equivalent pot temperature [K]')
    ax = add_topography(surface_p, latlon, time, ax, view)

    format_vert_plot(ax)
    create_title(ax, latlon, time, view)
    
    fig.savefig(path_temp, dpi=dpi)
    plt.close()
    # plt.show()


def plot_vertical_hum(ds, *, surface_p, masked_data, latlon, time, path_temp, view, colors= ['#7EDF7F', '#249527'], dpi=200):
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
    fig, ax = plot_vert_geopotential(ds, latlon=latlon, time=time, view=view)
    match view:
        case "vert_w_e":
            mesh = masked_data.sel(latitude=latlon, time=time).plot.contourf(levels=[0, 1, 2],
                                                                        colors=colors,
                                                                        add_colorbar=False,
                                                                        ax=ax)
        case "vert_n_s":
            mesh = masked_data.sel(longitude=latlon, time=time).plot.contourf(levels=[0, 1, 2],
                                                                        colors=colors,
                                                                        add_colorbar=False,
                                                                        ax=ax)
    ax = add_windbarbs(ds, latlon, time, ax, view)
    ax = add_topography(surface_p, latlon, time, ax, view)

    cbar = create_cbar_hum(ax, mesh)
    set_ticks_hum(cbar)
    format_vert_plot(ax)
    create_title(ax, param=latlon, time=time, view=view)
    fig.savefig(path_temp, dpi=dpi)
    plt.close()


def plot_vertical_cc(ds, *, surface_p, latlon, time, path_temp, cmap, view, dpi=200):
    """
    plots the vertical cuts of geopotential with cloud cover

    Parameters
    ----------
    latitude : longitude of dataset
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename

    Returns
    -------
    None

    """
    fig, ax = plot_vert_geopotential(ds, latlon=latlon, time=time, view=view)
    match view:
        case "vert_w_e":
            mesh_cc = ds.sel(latitude=latlon, time=time).cc.plot.contourf(ax=ax, cmap=cmap,
                                                                        add_colorbar=False)
        case "vert_n_s":
            mesh_cc = ds.sel(longitude=latlon, time=time).cc.plot.contourf(ax=ax, cmap=cmap,
                                                                        add_colorbar=False)

    ax = add_topography(surface_p, latlon, time, ax, view)

    plt.colorbar(mesh_cc, ax=ax, label='cloud cover fraction [0-1]')
    format_vert_plot(ax)
    create_title(ax, param=latlon, time=time, view=view)
    fig.savefig(path_temp, dpi=dpi)
    plt.close()
    # plt.show()


def create_view_dir(view):
    """
    create dir for view in upper folder if it doesn't exist yet
    """
    path = f"../era5{view}/"
    if not os.path.exists(path): 
        os.mkdir(path) 


def create_time_dir(view, time_str):
    """
    if directory for images does not yet exist, create it
    """
    path = f"../era5{view}/{time_str}/"
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def myround(x, base=5):
    """
    rounds x to next value with a 5 digit at the end
    """
    return base * round(x/base)


def define_params(ds):
    """
    define all important parameters for the plotting process, like quality of saved png files, distance between vertical cross sections, ...
    """
    contour_lvls_temp = 10; contour_lvls_cloud = 6
    lons = ds.longitude.values[::8]
    lats = lats = ds.latitude.values[::8]
    levels = np.array([300, 500, 700, 800, 850, 900, 950, 1000]) # ds.level.values[::2]
    times = ds.time.values
    
    vmin_c = myround(ds.t_c.min().values); vmax_c = myround(ds.t_c.max().values)
    vmin_pot = myround(ds.t_pot.min().values); vmax_pot = myround(ds.t_pot.max().values)
    vmin_eqpt = myround(ds.eqpt.min().values); vmax_eqpt = myround(ds.eqpt.max().values)

    cmap_cloud = plt.get_cmap('Blues', contour_lvls_cloud); cmap_temp = plt.get_cmap('coolwarm', contour_lvls_temp)
    colors_hum = ['#7EDF7F', '#249527']

    return contour_lvls_temp, contour_lvls_cloud, lons, lats, levels, times, vmin_c, vmax_c, vmin_pot, vmax_pot, vmin_eqpt, vmax_eqpt, cmap_cloud, cmap_temp, colors_hum


def plotting_era5(ds, surface_p, dpi=200, variables=["temp", "pot_temp", "eqpt", "hum", "cc"]):
    """
    main function for plotting everything, i know for loops look messy but with vectorization it looks even worse!
    """
    contour_lvls_temp, contour_lvls_cloud, lons, lats, levels, times, vmin_c, vmax_c, vmin_pot, vmax_pot, vmin_eqpt, vmax_eqpt, cmap_cloud, cmap_temp, colors_hum = define_params(ds)
    dpi = 200
    views = ["horiz", "vert_w_e", "vert_n_s"]
    masked_data = mask_hum(ds)

    for view in views:  # loop over horizontal, vertical w-e & vertical n-s plots
        create_view_dir(view)
        
        for time in times:  # loop over timestamp-folders: one folder for each timestamp; 
            time_str = pd.Timestamp(time).strftime("%Y%m%d_%H")  # convert time to str for saving
            current_dir = create_time_dir(view, time_str)  

            for var in variables:  # here begin plotting specific loops
                    # create different filename for different varibles, timestamps and levels
                    match view:
                        case "horiz":
                            for level in levels:
                                path_temp = current_dir + f'{time_str}_{level}_{view}_{var}.png'
                                if os.path.exists(path_temp): continue # if file already exists, skip plotting
                                match var:
                                    case "temp":
                                        plot_horizontal_temp(ds, level, time, path_temp, vmin_c, vmax_c, cmap_temp, contour_lvls_temp, dpi)
                                    case "pot_temp":
                                        plot_horizontal_pot_temp(ds, level, time, path_temp, vmin_pot, vmax_pot, cmap_temp, contour_lvls_temp, dpi)
                                    case "eqpt":
                                        plot_horizontal_equiv_pot_temp(ds, level=level, time=time, path=path_temp, vmin=vmin_eqpt, 
                                                                    vmax=vmax_eqpt, cmap=cmap_temp, contour_lvls_temp=10, dpi=dpi)
                                    case "hum":
                                        plot_horizontal_hum(ds, masked_data=masked_data, level=level, time=time, path=path_temp, colors=colors_hum, dpi=dpi)
                                    case "cc":
                                        plot_horizontal_cc(ds, level, time, path_temp, cmap_cloud, dpi)
                        case "vert_w_e":
                            for lat in lats:
                                path_temp = current_dir + f'{time_str}_{lat}_{view}_{var}.png'
                                if os.path.exists(path_temp): continue
                                match var:
                                    case "temp":
                                        plot_vertical_temp(ds, surface_p=surface_p, latlon=lat, time=time, path_temp=path_temp, cmap=cmap_temp, 
                                                        vmin=vmin_c, vmax=vmax_c, contour_lvls_temp=contour_lvls_temp, view=view, dpi=dpi)
                                    case "pot_temp":
                                        plot_vertical_pot_temp(ds, surface_p=surface_p, latlon=lat, time=time, path_temp=path_temp,
                                                                vmin=vmin_pot, vmax=vmax_pot, cmap=cmap_temp, contour_lvls_temp=contour_lvls_temp, view=view, dpi=dpi)
                                    case "eqpt":
                                        plot_vertical_equiv_pot_temp(ds, surface_p=surface_p, latlon=lat, time=time, path_temp=path_temp,
                                                                vmin=vmin_eqpt, vmax=vmax_eqpt, cmap=cmap_temp, contour_lvls_temp=contour_lvls_temp, view=view, dpi=dpi)
                                    case "hum":
                                        plot_vertical_hum(ds, surface_p=surface_p, masked_data=masked_data, latlon=lat, time=time, path_temp=path_temp, 
                                                            view=view, colors=colors_hum, dpi=dpi)
                                    case "cc":
                                        plot_vertical_cc(ds, surface_p=surface_p, latlon=lat, time=time, path_temp=path_temp, cmap=cmap_cloud, view=view, dpi=dpi)

                        case "vert_n_s":
                            for lon in lons:
                                path_temp = current_dir + f'{time_str}_{lon}_{view}_{var}.png'
                                if os.path.exists(path_temp): continue
                                match var:
                                    case "temp":
                                        plot_vertical_temp(ds, surface_p=surface_p, latlon=lon, time=time, path_temp=path_temp, cmap=cmap_temp, 
                                                        vmin=vmin_c, vmax=vmax_c, contour_lvls_temp=contour_lvls_temp, view=view, dpi=dpi)
                                    case "pot_temp":
                                        plot_vertical_pot_temp(ds, surface_p=surface_p, latlon=lon, time=time, path_temp=path_temp,
                                                                vmin=vmin_pot, vmax=vmax_pot, cmap=cmap_temp, contour_lvls_temp=contour_lvls_temp, view=view, dpi=dpi)
                                    case "eqpt":
                                        plot_vertical_equiv_pot_temp(ds, surface_p=surface_p, latlon=lon, time=time, path_temp=path_temp,
                                                                vmin=vmin_eqpt, vmax=vmax_eqpt, cmap=cmap_temp, contour_lvls_temp=contour_lvls_temp, view=view, dpi=dpi)
                                    case "hum":
                                        plot_vertical_hum(ds, surface_p=surface_p, masked_data=masked_data, latlon=lon, time=time, path_temp=path_temp, 
                                                            view=view, colors=colors_hum, dpi=dpi)
                                    case "cc":
                                        plot_vertical_cc(ds, surface_p=surface_p, latlon=lon, time=time, path_temp=path_temp, cmap=cmap_cloud, view=view, dpi=dpi)
