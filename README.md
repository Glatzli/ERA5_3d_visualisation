# ERA5 3d visualisation:
## Goal:
Enable 3d visualization of weather fronts. In teaching at ACINN the 3d view of fronts 
is only presented on slides. This tool should enable visualizing the ecmwf model data.

create a webpage with 3 plots of the ECMWF ERA5 Data: 
-  horizontal view
-  vertical west-east cut
-  vertical north-south cut 

![Alt text](/screenshots/era5_vis_0509_18.png?raw=true "advancing cold front to austria")
![Alt text](/screenshots/era5_vis_0512_00.png?raw=true "low southwest of austria")
![Alt text](/screenshots/era5_vis_0510_06_hum.png?raw=true "humidity chart")
![Alt text](/screenshots/era5_vis_cc.png?raw=true "cloud cover chart")


We included plots of potential temperature & geopotential with the corresponding wind vectors 
in each plane, temperature & geopotential, humidity and cloud coverage.

We also included the model topography of the ECMWF model to get an overview of the
mountain-related processes. 

For the data we used ERA5 Reanalysis data of the Copernicus site.
To create the webpage we used panel, a first draft was also done in via javascript as a string 
in python.


## Ideas for advancing:
-  optimize plots, legends and colors
-  
