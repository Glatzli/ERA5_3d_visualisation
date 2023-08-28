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
import metpy.calc as mpcalc
from metpy.units import units
from pint import UnitRegistry

import plotting_era5


def calc_temps(ds):
    """
    calculates temp in °C and pot temperature    
    """
    ds = ds.assign(t_c = ds["t"] - 273.15)
    # ds = ds.assign(t_pot = ds["t"] * (1000 / ds.level) ** (2 / 7))
    # manipulate rh: set vals>100% to 100 and vals < 0 to 0:
    # ds = ds.assign(rh = xr.where(ds['r'] > 100, ds["r"], 100)) 
    # ds = ds.assign(rh = xr.where(ds['r'] < 0, 0, ds["r"]))

    # ds = ds.assign(td = mpcalc.dewpoint_from_relative_humidity(temperature=ds.t_c*units.degC, relative_humidity=ds.rh))
    # mpcalc.equivalent_potential_temperature(pressure=ds.level*units.mbar, temperature=ds.t_c*units.degC, dewpoint=ds.td*units.degC)

    ureg = UnitRegistry()

    unit_w = ureg.Pa / ureg.second
    # computing vertical velocity assuming hydrostatic conditions on synoptic scale
    ds = ds.assign(mr = mpcalc.mixing_ratio_from_relative_humidity(ds.level*units.hpa, ds.t_c*units.degC, ds.r).to('g/kg'))
    mpcalc.vertical_velocity(ds.w*units.(Pa/s), ds.level*units.hpa, ds.t_c*units.degC, mixing_ratio=ds.mr)  

    ds = ds.assign(t_pot = mpcalc.potential_temperature(pressure=ds.level*units.mbar, temperature=ds.t_c*units.degC))  # pot temp in K

    return ds


if __name__ == '__main__':
    ds = xr.open_dataset(r'C:\Users\dgratzl\OneDrive - Austro Control GmbH\era5_data_may_v4.nc')
    ds = calc_temps(ds)
    # load model topography in Pa
    surface_p = xr.open_dataset(r'C:\Users\dgratzl\OneDrive - Austro Control GmbH\ERA\surface_p.nc')

    # plotting_era5.plotting_era5(ds, surface_p, dpi=200, variables=["temp", "pot_temp", "hum", "cc"])
