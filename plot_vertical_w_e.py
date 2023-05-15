# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:06:50 2023

@author: Surface Pro
"""

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# Load ERA5 data from NetCDF file
ds = xr.open_dataset('./')

# Select a vertical section of data
section = ds.sel(latitude=slice(60, 30), longitude=slice(-3, 27))

# Extract variables for plotting
z = section['z'] / 1000  # Convert geopotential height to kilometers
theta = section['theta']  # Potential temperature

# Create a vertical section plot
fig, ax = plt.subplots(figsize=(8, 6))

# Plot geopotential height as lines
ax.contour(z, colors='black', levels=np.arange(0, 20000, 500), linewidths=0.5)

# Plot potential temperature as filled contours
cs = ax.contourf(theta, cmap='coolwarm')

# Add colorbar
plt.colorbar(cs, ax=ax, label='Potential Temperature (K)')

# Set axes labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Pressure (hPa)')
ax.invert_yaxis()
ax.set_ylim(ax.get_ylim()[::-1])
ax.set_title('ERA5 Vertical Section')

plt.show()
