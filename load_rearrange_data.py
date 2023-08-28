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
    ureg = UnitRegistry()  # load units from pint (package for unit handling)
    # add new unit Pa/s to pint:
    # ureg = ureg.define("pascal_per_second = Pa / s = Paps")  # somehow this is not working?
    # subset dataset for calulation of equivalent pot temp, pot temp:
    ds_unit = ds[["t", "r", "u", "v", "w"]]
    ds_units = ds_unit.metpy.quantify()
    
    ds = ds.assign(t_c = ds["t"] - 273.15)
    
    # ds = ds.assign(t_pot = ds["t"] * (1000 / ds.level) ** (2 / 7))
    # manipulate rh: set vals>100% to 100 and vals < 0 to 0:
    # ds = ds.assign(rh = xr.where(ds['r'] > 100, ds["r"], 100)) 
    # ds = ds.assign(rh = xr.where(ds['r'] < 0, 0, ds["r"]))

    ds = ds.assign(td = mpcalc.dewpoint_from_relative_humidity(temperature=ds.t_c*units.degC, 
                                                               relative_humidity=ds.r*units.percent))
    
    ds = ds.assign(t_eqp = mpcalc.equivalent_potential_temperature(pressure=ds.level*units.mbar,
                                                      temperature=ds.t_c*units.degC, 
                                                      dewpoint=ds.td*units.degC))  #

    # computing vertical velocity assuming hydrostatic conditions on synoptic scale
    ds = ds.assign(mr = mpcalc.mixing_ratio_from_relative_humidity(
        ds.level*units.mbar, ds.t_c*units.degC, ds.r))  # .to('g/kg')
    
    # convert wind components from m/s to knots for plotting:
    ds["u"] = ds.u.metpy.convert_units("knots")
    ds["v"] = ds.v.metpy.convert_units("knots")
    ds = ds.assign(w_ms = mpcalc.vertical_velocity(ds.w, ds.level*units.mbar, ds.t_c*units.degC, 
                             mixing_ratio=ds.mr))  # *units.Paps; somehow the unit is not working?!?
    ds["w_knots"] = ds.w_ms.metpy.convert_units("knots")

    ds = ds.assign(t_pot = mpcalc.potential_temperature(
        pressure=ds.level*units.mbar, temperature=ds.t_c*units.degC))  # pot temp in K

    return ds


if __name__ == '__main__':
    # path_to_era5_project = "C:\Users\dgratzl\OneDrive - Austro Control GmbH\"
    # path_to_era5_project = "C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5-3d-visualisation"
    # total_path = os.path.join(path_to_era5_project, "era5_data_may_v4.nc")
    ds = xr.open_dataset(r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5_data_may_v4.nc')
    ds = calc_temps(ds)
    # load model topography in Pa
    surface_p = xr.open_dataset(r'C:\Users\Surface Pro\OneDrive\Dokumente\Uni\Programmieren_test_git\era5-3d-visualisation\surface_p.nc')

    # plotting_era5.plotting_era5(ds, surface_p, dpi=200, variables=["pot_temp", "hum", "cc"]) #"temp", 






