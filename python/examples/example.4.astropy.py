"""

## Meas/Coords Validation with Astropy

This goal of this example is to show that real data mapped on `Measure` classes can be transformed in Astropy instances in a transparent way.

We proceed with data mapped on individual `Measure` objects in order to avoid bias possibly introduced by some host model.

This workflow validates the [Measure](https://github.com/ivoa/modelinstanceinvot-code) model (and its coordinates(https://github.com/ivoa-std/CoordinateDM)) in the extand of the the implemented classes.


### Test Case

The VOtable has been queried from tme ESAC archive (https://gea.esac.esa.int/tap-server/tap) with the following query:
```
SELECT TOP 100 gaiadr2.gaia_source.designation, gaiadr2.gaia_source.ra, gaiadr2.gaia_source.ra_error ,
               gaiadr2.gaia_source.\"dec\", gaiadr2.gaia_source.dec_error, gaiadr2.gaia_source.parallax , 
               gaiadr2.gaia_source.parallax_error, gaiadr2.gaia_source.pmra, 
               gaiadr2.gaia_source.pmra_error, gaiadr2.gaia_source.pmdec, 
               gaiadr2.gaia_source.pmdec_error,gaiadr2.gaia_source.radial_velocity, 
               gaiadr2.gaia_source.radial_velocity_error
 FROM  gaiadr2.gaia_source
 WHERE ( CONTAINS(POINT('ICRS', ra, \"dec\"), 
         CIRCLE('ICRS', 162.328814, -53.319466, 0.016666666666666666)) = 1 )
```

We select positions, parallax, radial velocity and proper motions around `luhman 16`. 

The goal of the script is to show how we can build complex Astropy SkyCoord object in a transparent way by using the `Meas/Coords` mapping. 
The parallax is given to Astropy to build the 3rd coordinate dimension. 
There no data checking, for each row, all mapped STC components are built and given to the SkyCoord builder which does its best.
    
- We are using the annotation [syntax](https://github.com/ivoa-std/ModelInstanceInVot) that has been designed after the 2021 workshop.
- The Python code used for this notebook is being [developped](https://github.com/ivoa/modelinstanceinvot-code) to design qnd validate the processing of model annotation.
- This notebook does not pretend to have any scientific value, it is juste a validation case for the mapping syntax
 
 
Created on Jan 26, 2022

@author: laurentmichel
"""
import os
import logging
import matplotlib
import mplcursors
import matplotlib.pyplot as plt 
import numpy as np
from astropy.io.votable import parse
from astropy.visualization import astropy_mpl_style

from client.xml_interpreter.model_viewer import ModelViewer

plt.style.use(astropy_mpl_style)
matplotlib.font_manager: logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)

# Connect the VOTable and parse the annotations
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
votable = parse(os.path.join(data_path, "gaia_luhman16_astropy.xml"))
for resource in votable.resources:
    mviewer = ModelViewer(resource, votable_path=os.path.join(data_path, "gaia_luhman16_astropy.xml"))
    mviewer.connect_table('Results')
    break;

tooltips = []
ras = []
decs = []
dist = []

while True:
    # get a data row (numpy)
    row = mviewer.get_next_row() 
    if row is None:
        break  
    # get the astropy SkyCoord object for that row
    position = mviewer.get_astropy_sky_coord()    
    # stores the parameters to be plotted  
    # Ignore not set-distances and limit the distance range for the plot readability      
    if not np.isnan(position.distance.value) and position.distance.value < 5000.0:
        ras.append(position.ra.value)    
        decs.append(position.dec.value)   
        dist.append(position.distance.value)   
        tooltips.append(f"Proper Motion ra:{position.pm_ra_cosdec:.2f} \ndec:{position.pm_dec:.2f} ")
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(ras, decs, dist)
ax.set_xlabel('RA')
ax.set_ylabel('DEC')
ax.set_zlabel('Dist (parsec)')
mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(tooltips[sel.index]))
plt.show()
 


