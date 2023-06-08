import os
from pathlib import Path



def generate_era5_visualization(timestamps, levels):
    html_code = f'''<!DOCTYPE html>
    <html>
    <head>
      <title>ERA5 Data Visualization</title>
      <style>
        /* CSS styling */
        .slider-container {{
          width: 600px;
          margin: 20px auto;
        }}
        img {{
          display: block;
          margin: 0 auto;
          max-width: 600px;
        }}
      </style>
    </head>
    <body>
      <h1>ERA5 Data Visualization</h1>
      
      <div class="slider-container">
        <p>Select Timestamp:</p>
        <input type="range" id="timestamp-slider" min="0" max="{len(timestamps) - 1}" step="1" value="0">
      </div>
      
      <div class="slider-container">
        <p>Select Level:</p>
        <input type="range" id="level-slider" min="0" max="{len(levels) - 1}" step="1" value="0">
      </div>
      
      <img id="plot-image" src="">
    
      <script>
        // JavaScript code
        const timestampSlider = document.getElementById('timestamp-slider');
        const levelSlider = document.getElementById('level-slider');
        const plotImage = document.getElementById('plot-image');
    
        // Define the timestamps and levels
        let timestamps = {timestamps};
        let levels = {levels};
        
        let timestampIndex = parseInt(timestampSlider.value);
        let levelIndex = parseInt(levelSlider.value);

        // Update the displayed plot when the slider values change
        timestampSlider.addEventListener('input', function() {{
          timestampIndex = parseInt(timestampSlider.value);
          const imagePath = generateImagePath(timestamps[timestampIndex], levels[levelIndex]);
          plotImage.src = imagePath;
        }});
        
        levelSlider.addEventListener('input', function() {{
          const levelIndex = parseInt(levelSlider.value);
	      const imagePath = generateImagePath(timestamps[timestampIndex], levels[levelIndex]);
          plotImage.src = imagePath;
        }});
        
        // Set the initial plot image
        const initialImagePath = generateImagePath(timestamps[0], levels[0]);
        plotImage.src = initialImagePath;
        
        function generateImagePath(timestamp, level) {{
            const filepath = '../era5horiz_plots/' + timestamp + '/' + timestamp + '_' + level + '_era5_horiz.png';
            return filepath;
        }}
        </script>
    </body>
    </html>'''

    # Write the HTML code to a file
    with open('era5_visualization.html', 'w') as f:
        f.write(html_code)
        
def sortby(x):
    try:
        return int(x.split('_')[2])
    except ValueError:
        return float('inf')


folders = os.listdir("../era5horiz_plots/")  # list all folders
timestamps = []; levels = []

for folder in folders: # loop over all timestamp-folders
    timestamps.append(folder)
    files = os.listdir(os.path.join("../era5horiz_plots/", folder))
    files.sort(key=sortby)
    
    for file in files: # loop over all level plots in one dir
        level = file.split('_')[2]
        if level not in levels:
            levels.append(level)

generate_era5_visualization(timestamps, levels)

