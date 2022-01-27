"""
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
 


