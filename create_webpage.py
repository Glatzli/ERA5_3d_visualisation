import os

def generate_era5_visualization(num_plots, image_paths):
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
    </head>
    <body>
      <h1>ERA5 Data Visualization</h1>
      
      <div class="slider-container">
        <input type="range" id="slider" min="0" max="{num_plots - 1}" step="1" value="0">
      </div>
      
      <img id="plot-image" src="{image_paths[0]}">
    
      <script>
        // JavaScript code
        const slider = document.getElementById('slider');
        const plotImage = document.getElementById('plot-image');
    
        // Define the number of plots and their image paths
        const numPlots = {num_plots};
        const plotImagePaths = {image_paths};
    
        // Update the displayed plot when the slider value changes
        slider.addEventListener('input', function() {{
          const plotIndex = parseInt(slider.value);
          const imagePath = plotImagePaths[plotIndex];
          plotImage.src = imagePath;
        }});
      </script>
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

image_paths = []
levels = []
timestamps = []
for file in files: # create lists with all levels, timestamps and filepaths
    levels.append(file.split('_')[1])
    timestamps.append(file.split('_')[0])
    image_paths.append("../era5horiz_plots/" + file)
    
# make function to create a list of strings to all horizontal plots as png files

num_plots = len(files)

generate_era5_visualization(num_plots, image_paths)
