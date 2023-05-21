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
w = ds.isel(latitude=40, time=5).w

lvl_interp = np.linspace(lvl.min(), lvl.max(), len(lon))
u_interp = np.interp(lvl_interp, lvl, u.level)
w_interp = np.interp(lvl_interp, lvl, w.level)

ax.quiver(lon, lvl_interp, u_interp, w_interp)
#plt.yscale('log')
plt.show()
