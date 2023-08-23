"""
    ERA5 project: try to rearrange the code usefully:
    1 function for loading .nc files, 1 for defining variables (like dpi), 1 for calculating temp in °C, ...
"""
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from matplotlib.ticker import ScalarFormatter

import plotting_era5


def calc_temps(ds):
    """
    calculates temp in °C and pot temperature    
    """
    ds = ds.assign(t_c = ds["t"] - 273.15)
    ds = ds.assign(t_pot = ds["t"] * (1000 / ds.level) ** (2 / 7))
    return ds


if __name__ == '__main__':
    ds = xr.open_dataset(r'C:\Users\dgratzl\OneDrive - Austro Control GmbH\era5_data_may_v4.nc')
    ds = calc_temps(ds)
    # load model topography in Pa
    surface_p = xr.open_dataset(r'C:\Users\dgratzl\OneDrive - Austro Control GmbH\ERA\surface_p.nc')

    plotting_era5.plotting_era5(ds, surface_p, dpi=200, variables=["temp", "pot_temp", "hum", "cc"])
