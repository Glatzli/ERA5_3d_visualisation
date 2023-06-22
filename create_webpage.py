import os

def generate_era5_visualization(timestamps, levels, lats, lons):
    html_code = f'''<!DOCTYPE html>
    <html>
    <head>
      <title>ERA5 Data Visualization</title>
      <style>
        /* CSS styling */
        .slider-container {{
          width: 200px;
          height: 10px;
          margin: 50px auto;
        }}
        .slider-vertical {{
          width: 10px;
          height: 200px;
        }}
        .slider-horizontal {{
          width: 200px;
          height: 10px;
          //margin: 20px auto;
        }}
        .image-container {{
          display: flex;
          //justify-content: center;
          width: 100%;
          max-width: 1500px;
          margin: 0 auto;
        }}
        .image-container img {{
          width: 50%;
          max-width: 100%;
          //height: auto;
        }}
      </style>
    </head>
    
    <body>
      <h1>ERA5 Data Visualization</h1>
      
      <div class="slider-container">
        <p>Timestamp: <output id="value"></output></p>
        <input type="range" id="timestamp-slider" min="0" max="{len(timestamps) - 1}" step="1" value="0">
      </div>
      <div class="slider-container">
        <p>level: <output id="level"></output> hpa</p>
        <input type="range" id="level-slider" min="0" max="{len(levels) - 1}" step="1" value="0">
      </div>
      
      <div class="image-container">
        <div class="slider-container">
          <p>latitude: <output id="lat"></output> °N</p>
          <input type="range" id="lat-vertical-slider" class="slider-vertical" min="0" max="{len(lats) - 1}" step="1" value="0" orient="vertical">
        </div>
        <img id="horiz_image" src="">
        <img id="vert_w_e_image" src="">
        <img id="vert_n_s_image" src="">
      </div>
      
      <div class="slider-container">
        <p>longitude: <output id="lon"></output></p>
        <input type="range" id="lon-horizontal-slider" class="slider-horizontal" min="0" max="{len(lons) - 1}" step="1" value="0">
      </div> 
      
      <script>
        const timestampSlider = document.getElementById('timestamp-slider');
        const levelSlider = document.getElementById('level-slider');
        const latSlider = document.getElementById('lat-vertical-slider');
        const lonSlider = document.getElementById('lon-horizontal-slider');
        const horiz_image = document.getElementById('horiz_image');
        const vert_w_e_image = document.getElementById('vert_w_e_image');
        const vert_n_s_image = document.getElementById('vert_n_s_image');
    
        // Define the timestamps and levels
        let timestamps = {timestamps};
        let levels = {levels};
        let lats = {lats};
        let lons = {lons};
        
        let timestampIndex = parseInt(timestampSlider.value);
        let levelIndex = parseInt(levelSlider.value);
        let latIndex = parseInt(latSlider.value);
        let lonIndex = parseInt(lonSlider.value);

        // Update the displayed plot when the slider values change
        timestampSlider.addEventListener('input', function() {{
          timestampIndex = parseInt(timestampSlider.value);
          value.textContent = timestamps[timestampIndex];
          horiz_image.src = horiz_path(timestamps[timestampIndex], levels[levelIndex]);
          vert_w_e_image.src = vert_w_e_path(timestamps[timestampIndex], lats[latIndex]);
          vert_n_s_image.src = vert_n_s_path(timestamps[timestampIndex], lons[lonIndex]);
        }});
        
        levelSlider.addEventListener('input', function() {{
          const levelIndex = parseInt(levelSlider.value);
          level.textContent = levels[levelIndex];
	      horiz_image.src = horiz_path(timestamps[timestampIndex], levels[levelIndex]);
          vert_w_e_image.src = vert_w_e_path(timestamps[timestampIndex], lats[latIndex]);
          vert_n_s_image.src = vert_n_s_path(timestamps[timestampIndex], lons[lonIndex]);
        }});
        latSlider.addEventListener('input', function() {{
          const latIndex = parseInt(latSlider.value);
          lat.textContent = lats[latIndex];
	      horiz_image.src = horiz_path(timestamps[timestampIndex], levels[levelIndex]);
          vert_w_e_image.src = vert_w_e_path(timestamps[timestampIndex], lats[latIndex]);
          vert_n_s_image.src = vert_n_s_path(timestamps[timestampIndex], lons[lonIndex]);
        }});
        lonSlider.addEventListener('input', function() {{
          const lonIndex = parseInt(lonSlider.value);
          lon.textContent = lons[lonIndex];
	      horiz_image.src = horiz_path(timestamps[timestampIndex], levels[levelIndex]);
          vert_w_e_image.src = vert_w_e_path(timestamps[timestampIndex], lats[latIndex]);
          vert_n_s_image.src = vert_n_s_path(timestamps[timestampIndex], lons[lonIndex]);
        }});
        
        // Set the initial plot image
        horiz_image.src = horiz_path(timestamps[0], levels[0]);
        vert_w_e_image.src = vert_w_e_path(timestamps[0], lats[0]);
        vert_n_s_image.src = vert_n_s_path(timestamps[0], lons[0]);
        
        // new try
        const value = document.querySelector("#value");
        value.textContent = timestamps[0];
        const level = document.querySelector("#level");
        level.textContent = levels[0];
        const lat = document.querySelector("#lat");
        lat.textContent = lats[0];
        const lon = document.querySelector("#lon");
        lon.textContent = lons[0];
        
        function horiz_path(timestamp, level) {{
            return '../era5horiz/' + timestamp + '/' + timestamp + '_' + level + '_horiz_temp.png';
        }}
        function vert_w_e_path(timestamp, lat) {{
            return '../era5vert_w_e/' + timestamp + '/' + timestamp + '_' + lat + '_vert_w_e_temp.png';
        }}
        function vert_n_s_path(timestamp, lon) {{
            return '../era5vert_n_s/' + timestamp + '/' + timestamp + '_' + lon + '_vert_n_s_temp.png';
        }}
        </script>
    </body>
    </html>'''

    # Write the HTML code to a file
    with open('era5_visualization.html', 'w') as f:
        f.write(html_code)
        
def sortby(x):
    try:
        return float(x.split('_')[2])
    except ValueError:
        return float('inf')


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
    

generate_era5_visualization(timestamps, levels, lats, lons)
