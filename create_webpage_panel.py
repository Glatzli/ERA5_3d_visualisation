"""
write: 
    panel serve create_webpage_panel.py --show --autoreload
in command prompt to open the created webpage while in current directory
note: must be in directory where this file is saved
"""

import panel as pn
import os

def sortby(x):
    """
    splits string at _ and returns 2nd part of string

    Parameters
    ----------
    x : input string

    Returns
    -------
    part of splitted string, or ValueError

    """
    try:
        return float(x.split('_')[2])
    except ValueError:
        return float('inf')

# panel layout
pn.extension('tabulator', design='material', template='material', loading_indicator=True)

h = 500; w = 500; # height & width for image sizes
h_s = 20; w_s = 400 # height & width for sliders
margin = 10 # for spacing between components

# list all timestamp folders
time_folders = os.listdir("../era5horiz/")  
timestamps = []; levels = []; lats = []; lons = [];

# loop over all timestamp-folders
for time_folder in time_folders: 
    timestamps.append(time_folder)
    
    # create list with all horizontal filepaths
    files_horiz = os.listdir(os.path.join("../era5horiz/", time_folder))
    files_horiz_temp = [file for file in files_horiz if file.endswith("_temp.png")]
    files_horiz_temp.sort(key=sortby) # sort by ascending levels
    
    for horiz_temp_file in files_horiz_temp: # loop over all horizontal plots in one dir
        level = horiz_temp_file.split('_')[2]
        if level not in levels:
            levels.append(level)
    
    # same process for vertical west east figures
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
timestampSlider = pn.widgets.DiscreteSlider(name = 'timestamp YYYYMMDD_HH:', options = timestamps, 
                                            value=timestamps[0], width=w_s, height=h_s, margin=margin,
                                            tooltips = True) 
levelSlider = pn.widgets.DiscreteSlider(name = 'level [hpa]:', options = ["300", 
                                                                          "500", 
                                                                          "700", 
                                                                          "800", 
                                                                          "850", 
                                                                          "900", 
                                                                          "950", 
                                                                          "1000"], 
                                        value = levels[0], width=w_s, height=h_s, margin=(30, margin)) 

lonSlider = pn.widgets.DiscreteSlider(name = 'longitude °E:', options = lons, value = lons[0], 
                                      width=w_s, height=h_s, margin=(30, margin))
latSlider = pn.widgets.DiscreteSlider(name = 'latitude °N:', options = lats, value = lats[0], 
                                      width=w_s, height=h_s, margin=margin) 

# variable selection feature
variable_selection = pn.widgets.RadioBoxGroup(name='RadioBoxGroup', options=["geopotential, potential temperature & wind",
                                                                             "geopotential, temperature & wind",
                                                                             "geopotential & equivalent pot temp",
                                                                             "relativ humidity & wind",
                                                                             "cloud coverage"], inline=False)

# default variable is potential temperature
init_horiz_path = '../era5horiz/' + timestamps[0] + '/' + timestamps[0] + '_' + levels[0] + '_horiz_pot_temp.png'
init_vert_w_e_path = '../era5vert_w_e/' + timestamps[0] + '/' + timestamps[0] + '_' + lats[0] + '_vert_w_e_pot_temp.png'
init_vert_n_s_path = '../era5vert_n_s/' + timestamps[0] + '/' + timestamps[0] + '_' + lons[0] + '_vert_n_s_pot_temp.png'

# Define the PNG panes for plots, different margin for 3rd plot (variable selection above)
horiz_image = pn.pane.PNG(object=init_horiz_path, width = w, height = h, 
                             margin=(60, 0))
vert_w_e_image = pn.pane.PNG(object=init_vert_w_e_path, width = w, height = h, 
                             margin=(60, 0))
vert_n_s_image = pn.pane.PNG(object=init_vert_n_s_path, width = w, height = h, 
                             margin=(0, 0))


def update_file_path(event):
    """
    when changing a slider or switching between variables all the file paths & 
    graphics are updated accordingly

    Parameters
    ----------
    event : when a slider or the radioboxgroup changes

    Returns
    -------
    None.

    """
    timestamp = timestampSlider.value
    level = levelSlider.value
    lat = latSlider.value
    lon = lonSlider.value
    variable = variable_selection.value
    
    # when switching variable, change fileending
    match variable:
        case 'geopotential, potential temperature & wind':
            fileending = 'temp'
        case "geopotential, temperature & wind":
            fileending = "pot_temp"
        case "geopotential & equivalent pot temp":
            fileending = "eqpt"
        case "relativ humidity & wind":
            fileending = 'hum'
        case "cloud coverage":
            fileending = 'cc'
    
    # set filepaths
    horiz_image.object = '../era5horiz/' + timestamp + '/' + timestamp + '_' + level + '_horiz_' + fileending + '.png';
    vert_w_e_image.object = '../era5vert_w_e/' + timestamp + '/' + timestamp + '_' + lat + '_vert_w_e_' + fileending + '.png';
    vert_n_s_image.object = '../era5vert_n_s/' + timestamp + '/' + timestamp + '_' + lon + '_vert_n_s_' + fileending + '.png';
    
# watch over all parameters
timestampSlider.param.watch(update_file_path, 'value')
levelSlider.param.watch(update_file_path, 'value')
latSlider.param.watch(update_file_path, 'value')
lonSlider.param.watch(update_file_path, 'value')
variable_selection.param.watch(update_file_path, 'value')

# page setup with Rows&Columns from panel:
pn.Row(pn.Column(latSlider, lonSlider, horiz_image),
       pn.Column(timestampSlider, levelSlider, vert_w_e_image),
       pn.Column(variable_selection, vert_n_s_image), sizing_mode='stretch_both').servable()
