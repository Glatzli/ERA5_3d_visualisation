# ERA5 3d visualisation:
In the teaching at ACINN the 3D view of fronts is only presented on slides, the vertical component is 
therefore a bit unattended. This tool should help the students getting a 3D view of weather model data, 
primarily to visualize weather fronts. It should enable the students to get a better 3D understanding 
of the processes in the atmosphere.

This tool creates a webpage with 3 plots of the ECMWF ERA5 Data: 
-  horizontal view
-  vertical west-east cut
-  vertical north-south cut

The user of the webpage can change the latitude/longitude where the cutlines should be via sliders.
The following screenshots of the webpage are with data during a coldfront approach and Low formation 
south of Austria from May 2023:
![Alt text](/screenshots/temp2.png?raw=true "advancing cold front to austria 09.05. 06:00")
![Alt text](/screenshots/hum2.png?raw=true "humidity chart 09.05. 06:00")
![Alt text](/screenshots/cloud2.png?raw=true "cloud cover chart 09.05. 06:00")
![Alt text](/screenshots/temp3.png?raw=true "pot temp&geopotential 10.05. 00:00")
![Alt text](/screenshots/hum3.png?raw=true "humidity chart 09.05. 06:00")
![Alt text](/screenshots/temp4.png?raw=true "pot temp&geopotential 10.05. 00:00")
![Alt text](/screenshots/hum4.png?raw=true "humidity chart 09.05. 06:00")
![Alt text](/screenshots/cloud4.png?raw=true "cloud cover chart 09.05. 06:00")


We included plots of potential temperature & geopotential with the corresponding wind vectors 
in each plane, temperature & geopotential, humidity and cloud coverage.

We also included the model topography of the ECMWF model to get an overview of the
mountain-related processes. 

For the data we used ERA5 Reanalysis data of the Copernicus (https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form)
site. To create the webpage we used panel, a first draft was also done in via javascript as a string in python.

All the plots are created beforehand locally, and are just displayed by the webpage.

#### Note that this tool is just a first draft and not fully developed!


## Ideas for advancing:
- calculate & plot vertical wind correctly? right now it is calculated via metpy, which is assuming hydrostatic conditions on synoptic scale. This is not the case for such a small-scale visualization!
- 
- add equivalent pot temp plots (with metpy calc, had problem with calculation of Td, rh sometimes > 100%, or smaller than 0!)
- optimize the webpage display: 
- display of time in proper format (right now the plots are scrolled changed by a discreteslider
using the name of the plots, f.e. the date is shown as the string by which the file is saved!)
- save the plots as vectorgraphics? we used pixelgraphics because it is already lasting quite a while for plotting all of them,
 but the wind arrows look messy!
- display the cutting-lines in the horizontal plot (probably only possible when doing the cut in realtime, 
which makes the webpage probably really slow! good example from panel: MRI Slicer)
- automate the data download to make the tool working with forecast data
- everything else you can think of!


