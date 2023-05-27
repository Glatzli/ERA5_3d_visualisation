import json

def create_era5_webpage(levels, times, image_path_format):
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
      const slider = document.getElementById('slider');
      const plotImage = document.getElementById('plot-image');

      // Define the levels and number of times
      const levels = {levels};

      // Update the displayed plot when the slider value changes
      slider.addEventListener('input', function() {{
        const levelIndex = parseInt(slider.value);
        const level = levels[levelIndex];
        const imagePath = "{image_path_format}".replace("{level}", levels[levelIndex]).replace("time", 0);
        plotImage.src = imagePath;
      }});

      // Set the initial plot image
      const initialImagePath = "{image_path_format}"//.replace("level", levels[0]).replace("{time}", 0);
      plotImage.src = initialImagePath;
    }}
  </script>
</head>
<body onload="updatePlot()">
  <h1>ERA5 Data Visualization</h1>

  <div class="slider-container">
    <input type="range" id="slider" min="0" max="{len(levels) - 1}" step="1" value="0">
  </div>

  <img id="plot-image">
</body>
</html>'''

    # Write the HTML code to a file
    with open('era5_visualization.html', 'w') as f:
        f.write(html_code)


# Usage example
levels = ['4', '6', '8']
times = ['5']

image_path_format = "../era5_plots/era5_horiz_l{level}_t{time}.png"
create_era5_webpage(levels, times, image_path_format)