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
from pathlib import Path

import plotting_era5


def calc_temps(ds):
    """
    calculates temp in °C and pot temperature    
    """
    ureg = UnitRegistry()  # load units from pint (package for unit handling)
    # add new unit Pa/s to pint:
    # ureg = ureg.define("pascal_per_second = Pa / s = Paps")  # somehow this is not working?
    # subset dataset for calulation of equivalent pot temp, pot temp:
    ds_units = ds[["t", "r", "u", "v", "w"]]
    # mask relative humidity 'cause it's sometimes > 100:
    ds_units["r"] = ds_units["r"].where(ds_units["r"] < 100) # , 100, ds_units["r"]
    ds_units["r"] = ds_units["r"].where(ds_units["r"] > 0)
    ds_units = ds_units.metpy.quantify()
    ds_units["t_c"] = ds_units["t"].metpy.convert_units('degC')

    ds_units["td"] = mpcalc.dewpoint_from_relative_humidity(temperature=ds_units["t_c"], relative_humidity=ds_units["r"])
    ds_units["eqpt"] = mpcalc.equivalent_potential_temperature(pressure=ds_units.level*units.mbar, temperature=ds_units["t_c"], dewpoint=ds_units["td"])
    
    # ds = ds.assign(t_c = ds["t"] - 273.15)
    # ds = ds.assign(t_pot = ds["t"] * (1000 / ds.level) ** (2 / 7))
    # manipulate rh: set vals>100% to 100 and vals < 0 to 0:
    # ds = ds.assign(rh = xr.where(ds['r'] > 100, ds["r"], 100)) 
    # ds = ds.assign(rh = xr.where(ds['r'] < 0, 0, ds["r"]))
    # ds = ds.assign(td = mpcalc.dewpoint_from_relative_humidity(temperature=ds.t_c*units.degC, relative_humidity=ds.r*units.percent))
    # ds = ds.assign(t_eqp = mpcalc.equivalent_potential_temperature(pressure=ds.level*units.mbar, temperature=ds.t_c*units.degC, dewpoint=ds.td*units.degC))

    # computing vertical velocity assuming hydrostatic conditions on synoptic scale
    ds_units["mr"] = mpcalc.mixing_ratio_from_relative_humidity(ds_units.level*units.mbar, ds_units.t_c, ds_units.r)
    
    # convert wind components from m/s to knots for plotting:
    ds_units["u_kt"] = ds_units.u.metpy.convert_units("knots")
    ds_units["v_kt"] = ds_units.v.metpy.convert_units("knots")
    ds_units["w_ms"] = mpcalc.vertical_velocity(ds_units.w, ds_units.level*units.mbar, ds_units.t_c, mixing_ratio=ds_units.mr) 
    ds_units["w_kt"] = ds_units.w_ms.metpy.convert_units("knots")

    ds_units["t_pot"] = mpcalc.potential_temperature(pressure=ds_units.level*units.mbar, temperature=ds_units.t_c)  # pot temp in K
    ds_units = ds_units.metpy.dequantify()
    ds = ds.assign(t_c = ds_units["t_c"], t_pot = ds_units["t_pot"], eqpt = ds_units["eqpt"],
                   u_kt = ds_units["u_kt"], v_kt = ds_units["v_kt"], w_kt = ds_units["w_kt"])

    return ds


if __name__ == '__main__':
    p = Path().resolve()  # get current wd
    # relative_path_to_copernicus_era5_data = Path("")   
    surface_p = xr.open_dataset(p / "surface_p.nc") # load model topography in Pa, with relative path from pathlib lib
    ds = xr.open_dataset(p.parent / "era5_data_may_v4.nc")

    ds = calc_temps(ds)

    plotting_era5.plotting_era5(ds, surface_p, dpi=200, variables=["pot_temp", "hum", "cc"]) #"temp", 

