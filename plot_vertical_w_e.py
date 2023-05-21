# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:06:50 2023

@author: Surface Pro
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Load ERA5 data from NetCDF file
ds = xr.open_dataset('C:/Users/Surface Pro/OneDrive/Dokumente/Uni/Programmieren_test_git/era5_data_april_v1.nc')


# Create a horizontal
fig, ax = plt.subplots(figsize=(8, 6))

ds.isel(level=5, time=5).z.plot.contour(ax= ax, colors='k')
ds.isel(level=5, time=5).t.plot.contourf(ax= ax, levels=10, cmap='coolwarm')
# Add colorbar
plt.colorbar(ax=ax, label='Temperature (K)')

# Create a vertical cross section
fig, ax = plt.subplots(figsize=(8, 6))

ds.isel(latitude=2, time=5).z.plot.contour(ax= ax, colors='k')
ds.isel(latitude=2, time=5).t.plot.contourf(ax= ax, levels=10, cmap='coolwarm')
# Add colorbar
plt.colorbar(ax=ax, label='Temperature (K)')

plt.show()
