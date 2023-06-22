import datetime as dt
import panel as pn
import os
import param
from PIL import Image, ImageDraw

import holoviews as hv
from bokeh.models import Div

import sys

# write: panel serve create_webpage_panel.py --show --autoreload
# in prompt to open the created webpage while in current directory

def sortby(x):
    try:
        return float(x.split('_')[2])
    except ValueError:
        return float('inf')

pn.extension('tabulator', design='material', template='material', loading_indicator=True)

h = 500; w = 500; # height&width for image sizes
h_s = 20; w_s = 400 # height&width for sliders
margin = 10 # for spacing between components

time_folders = os.listdir("../era5horiz/")  # list all time folders, same timestamps for all 3 plots assumed
timestamps = []; levels = []; lats = []; lons = [];

for time_folder in time_folders: # loop over all timestamp-folders
    timestamps.append(time_folder)
    files_horiz = os.listdir(os.path.join("../era5horiz/", time_folder))
    files_horiz_temp = [file for file in files_horiz if file.endswith("_temp.png")]
    
    files_horiz_temp.sort(key=sortby)
    
    for horiz_temp_file in files_horiz_temp: # loop over all level plots in one dir
        level = horiz_temp_file.split('_')[2]
        if level not in levels:
            levels.append(level)
    
    files_vert_w_e = os.listdir(os.path.join("../era5vert_w_e/", time_folder))
    files_vert_w_e.sort(key=sortby)
    for vert_w_e in files_vert_w_e: # loop over all lats
        lat = vert_w_e.split('_')[2]
        if lat not in lats:
            lats.append(lat)
    
    files_vert_n_s = os.listdir(os.path.join("../era5vert_n_s/", time_folder))
    files_vert_n_s.sort(key=sortby)
    for vert_n_s in files_vert_n_s: # loop over all lats
        lon = vert_n_s.split('_')[2]
        if lon not in lons:
            lons.append(lon)

pn.extension()

# setup widgets, for level&lon slider different height margins (because in 2nd line):
timestampSlider = pn.widgets.DiscreteSlider(name = 'timestamp:', options = timestamps, 
                                            value=timestamps[0], width=w_s, height=h_s, margin=margin) 
levelSlider = pn.widgets.DiscreteSlider(name = 'level:', options = levels, value = levels[0],
                                        width=w_s, height=h_s, margin=(30, margin)) 

lonSlider = pn.widgets.DiscreteSlider(name = 'longitude:', options = lons, value = lons[0], 
                                      width=w_s, height=h_s, margin=(30, margin))
latSlider = pn.widgets.DiscreteSlider(name = 'latitude:', options = lats, value = lats[0], 
                                      width=w_s, height=h_s, margin=margin) 
    
init_horiz_path = '../era5horiz/' + timestamps[0] + '/' + timestamps[0] + '_' + levels[0] + '_horiz_temp.png'

# Define the PNG pane
horiz_image = pn.pane.PNG(object=init_horiz_path, width = w, height = h)
vert_w_e_image = pn.pane.PNG(object='../era5vert_w_e/' + timestamps[0] + '/' + 
                             timestamps[0] + '_' + lats[0] + '_vert_w_e_temp.png', 
                             width = w, height = h)
vert_n_s_image = pn.pane.PNG(object='../era5vert_n_s/' + timestamps[0] + '/' + 
                             timestamps[0] + '_' + lons[0] + '_vert_n_s_temp.png', 
                             width = w, height = h, margin=(50, 0))


def update_file_path(event):
    """
    when changing a slider value all the file paths & graphics are updated 
    accordingly

    Parameters
    ----------
    event : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    timestamp = timestampSlider.value
    level = levelSlider.value
    lat = latSlider.value
    lon = lonSlider.value
    
    horiz_image.object = '../era5horiz/' + timestamp + '/' + timestamp + '_' + level + '_horiz_temp.png';
    vert_w_e_image.object = '../era5vert_w_e/' + timestamp + '/' + timestamp + '_' + lat + '_vert_w_e_temp.png';
    vert_n_s_image.object = '../era5vert_n_s/' + timestamp + '/' + timestamp + '_' + lon + '_vert_n_s_temp.png';
    

timestampSlider.param.watch(update_file_path, 'value')
levelSlider.param.watch(update_file_path, 'value')
latSlider.param.watch(update_file_path, 'value')
lonSlider.param.watch(update_file_path, 'value')

# page setup:
pn.Row(pn.Column(timestampSlider, levelSlider, horiz_image),
       pn.Column(latSlider, lonSlider, vert_w_e_image),
       pn.Column(vert_n_s_image), sizing_mode='stretch_both').servable()
