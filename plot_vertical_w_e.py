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
    r'C:\Users\Timm\Desktop\Atmospheric Sciences\Semester 2\Advanced Programming\era5_data_april_v1.nc')

# Create a horizontal
fig, ax = plt.subplots(figsize=(8, 6))

ds.isel(latitude=40, time=5).t.plot.contour(ax=ax, colors='k')
ds.isel(latitude=40, time=5).t.plot.contourf(ax=ax, levels=10, cmap='coolwarm')

lon = ds.isel(latitude=40, time=5).longitude
lvl = ds.isel(latitude=40, time=5).level
u = ds.isel(latitude=40, time=5).u
omega = ds.isel(latitude=40, time=5).w


R = 287.05
rho = lvl / (R*ds.isel(latitude=40, time=5).t)
w = - (omega/rho)

u = u/np.sqrt(u**2+w**2)
w = w/np.sqrt(u**2+w**2)

skip = dict(longitude=slice(None,None,10))
plt.quiver(lon[::10], lvl, u[skip], w[skip], color='black', scale=40, headwidth=2, headlength=3.5)


ax.invert_yaxis()

plt.yscale('log')
plt.show()
