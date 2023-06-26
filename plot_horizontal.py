import xarray as xr
import matplotlib
#matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os


def create_fig_national_boundaries():
    """
    create a figure with national boundaries of central europe

    Returns
    -------
    fig : figure handle
    ax : axis handle
    """
    # Create a horizontal
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
    
    # ax.set_xlabel('longitude'); ax.set_ylabel("latitude") #doesn't work!
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

def plot_horizontal_geopotential(level, time, fig, ax):
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

def plot_horizontal_temp(level, time, path, pot):
    """
    plot geopotential and temp and save it

    Parameters
    ----------
    level : height level [hpa]
    time : current timestamp (dimension value of dataset)
    path : path to current file incl. corresponding filename
    pot : boolean for using potential temperature or temperature

    Returns
    -------
    None.

    """
    fig, ax = create_fig_national_boundaries()
    fig, ax = plot_horizontal_geopotential(level, time, fig, ax)
       
    if pot:
        vmin = myround(np.min(ds.t_pot.values)) # round to next 
        vmax = myround(np.max(ds.t_pot.values))
        
        mesh_t = ds.sel(level=level, time=time).t_pot.plot.contourf(ax= ax,
                                                     cmap=cmap_temp,
                                                     levels=np.arange(vmin,  vmax, 5),
                                                     vmin = vmin, vmax = vmax,
                                                     add_colorbar = False)

        plt.colorbar(mesh_t, ax=ax, label='pot temperature [K]')
    elif ~pot:  
        if level <= 250: # set min/maxs of colormap according to pressure level
            vmax = -25; vmin = -85
        elif level <= 350:
            vmax = -15; vmin = -75
        elif level <= 400:
            vmax = -5; vmin = -65
        elif level <= 500:
            vmax = 10; vmin = -50
        elif level <= 700:
            vmax = 25; vmin = -35
        elif level <= 800:
            vmax = 30; vmin = -30
        elif level <= 850:
            vmax = 35; vmin = -25
        elif level <= 925:
            vmax = 40; vmin = -20
        else:
            vmax = 45; vmin = -15
        mesh_t = ds.sel(level=level, time=time).t_c.plot.contourf(ax= ax, levels=np.arange(vmin,  vmax, 5), 
                                                     cmap=cmap_temp, vmin=vmin, vmax=vmax,
                                                     add_colorbar = False)
        plt.colorbar(mesh_t, ax=ax, label='temperature [°C]')
    ax.set_title(f"level = {level}, time = {str(time).split(':')[0]}")
    
    fig.savefig(path, dpi=dpi)
    plt.close()

    
def plot_horizontal_hum(level, time, path):
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
    fig, ax = plot_horizontal_geopotential(level, time, fig, ax)    
    
    # Apply the masks to the data variable
    masked_data = xr.where(ds['r'] > 90, 2, xr.where(ds['r'] > 75, 1, np.nan))
    
    # Create the contourf plot using xarray's plot function
    mesh = masked_data.sel(level=level, time=time).plot.contourf(levels=[0, 1, 2], 
                                                                 colors=['#7EDF7F', '#249527'], 
                                                                 add_colorbar=False, 
                                                                 ax=ax)
    cbar = plt.colorbar(mesh, ax=ax, shrink=0.5, label='relative Humidity [%]')
    cbar.set_ticks([0.5, 1.5])
    cbar.set_ticklabels(['> 75', '> 90'])
    ax.set_title(f"level = {level}hPa, time = {str(time).split(':')[0]}")
    fig.savefig(path, dpi=dpi)
    plt.close()
    
def plot_horizontal_cc(level, time, path):  
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
    fig, ax = plot_horizontal_geopotential(level, time, fig, ax)
    mesh_cc = ds.sel(level=level, time=time).cc.plot.contourf(ax= ax, cmap=cmap_cloud, 
                                                       add_colorbar = False)
    plt.colorbar(mesh_cc, ax=ax, label='cloud cover fraction [0-1]')
    ax.set_title(f"level = {level}hPa, time = {str(time).split(':')[0]}")
    fig.savefig(path, dpi=dpi)
    plt.close()
    #plt.show()

    
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
    """
    round to next value, default is 5

    Parameters
    ----------
    x : input var
    base : next value to which to round. Default is 5.

    Returns
    -------
    rounded value
        
    Example:
        x = 8
        myround(x) 
        gives: 10

    """
    return base * round(x/base)
    

# Load ERA5 data from local NetCDF file
ds = xr.open_dataset(r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5_data_may_v4.nc')
ds = ds.assign(t_c = ds["t"] - 273.15) # temp in °C
ds = ds.assign(t_pot = ds["t"] * (1000 / ds.level) ** (2 / 7))

dpi = 100 # quality of saved png pics
# extract time and level dimensions from dataset
levels = ds.level.values[::2]
times = ds.time.values

contour_lvls = 10 # different colors & levels for temp plot
cmap_temp = plt.get_cmap('RdBu_r', contour_lvls)
cmap_cloud = plt.get_cmap('Blues', 6)
variables = ["temp", "pot_temp", "hum", "cc"]

# loop over timestamp-folders: one folder for each timestamp
for time in times:
    time_str = pd.Timestamp(time).strftime("%Y%m%d_%H") # convert time to str for saving
    
    # if directory for images does not yet exist, create it
    if not os.path.exists("../era5horiz/"): 
        os.mkdir("../era5horiz/") 
    if not os.path.exists(f"../era5horiz/{time_str}/"):
        os.mkdir(f"../era5horiz/{time_str}/")
    current_dir = f"../era5horiz/{time_str}/"  
         
    # loop over variables and levels for horizontal plot
    for var in variables:
        for level in levels:
            # create different filename for different varibles, timestamps and levels
            path_temp = current_dir + f'{time_str}_{level}_horiz_{var}.png'
            if os.path.exists(path_temp): # if file already exists, skip plotting
                continue
            
            # call plotting functions
            if var == "temp":
                plot_horizontal_temp(level, time, path_temp, pot = False)
            elif var == "pot_temp":
                plot_horizontal_temp(level, time, path_temp, pot = True)
            elif var == "hum":
                plot_horizontal_hum(level, time, path_temp)
            elif var == "cc":
                plot_horizontal_cc(level, time, path_temp)
