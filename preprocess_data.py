import datetime
import os
import json

def generate_era5_visualization(levels, times, image_path_format):
    # Generate the HTML code
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
  <script>
    // JavaScript code
    function updatePlot() {{
      const levelSlider = document.getElementById('level-slider');
      const timeSlider = document.getElementById('time-slider');
      const plotImage = document.getElementById('plot-image');

      // Define the levels and times
      const levels = {json.dumps(levels)};
      const times = {json.dumps(times)};

      // Update the displayed plot when the slider values change
      levelSlider.addEventListener('input', function() {{
        const levelIndex = parseInt(levelSlider.value);
        const timeIndex = parseInt(timeSlider.value);
        const imagePath = generateImagePath(levels[levelIndex], times[timeIndex]);
        plotImage.src = imagePath;
      }});
      
      timeSlider.addEventListener('input', function() {{
        const levelIndex = parseInt(levelSlider.value);
        const timeIndex = parseInt(timeSlider.value);
        const imagePath = generateImagePath(levels[levelIndex], times[timeIndex]);
        plotImage.src = imagePath;
      }});

      // Set the initial plot image
      const initialImagePath = generateImagePath(levels[0], times[0]);
      plotImage.src = initialImagePath;
    }}
    
    function generateImagePath(level, time) {{
      const currentDate = new Date();
      const year = currentDate.getUTCFullYear();
      const month = String(currentDate.getUTCMonth() + 1).padStart(2, '0');
      const day = String(currentDate.getUTCDate()).padStart(2, '0');
      const hours = String(currentDate.getUTCHours()).padStart(2, '0');
      return `$year$month$day_$hours_$level_era5_horiz.png`;
    }}
  </script>
</head>
<body onload="updatePlot()">
  <h1>ERA5 Data Visualization</h1>

  <div class="slider-container">
    <p>Select Level:</p>
    <input type="range" id="level-slider" min="0" max="{len(levels) - 1}" step="1" value="0">
  </div>
  
  <div class="slider-container">
    <p>Select Time:</p>
    <input type="range" id="time-slider" min="0" max="{len(times) - 1}" step="1" value="0">
  </div>

  <img id="plot-image">
</body>
</html>'''

    # Write the HTML code to a file
    with open('era5_visualization.html', 'w') as f:
        f.write(html_code)

files = os.listdir("../era5horiz_plots/") # list all 

def sortby(x):
    try:
        return int(x.split('_')[1])
    except ValueError:
        return float('inf')

files.sort(key=sortby)

# Usage example
levels = [1000, 850, 700, 500]
times = ['00', '06', '12', '18']
image_path_format = "../era5horiz_plots/{2023}{05}{08}_{00}_{level}_era5_horiz.png"
generate_era5_visualization(levels, times, image_path_format)
