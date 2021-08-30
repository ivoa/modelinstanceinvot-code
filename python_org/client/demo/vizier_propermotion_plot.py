'''

Read an annotated VOTABLE and show different outputs
Created on 31 mars 2020

@author: laurentmichel
'''

import os, sys
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
from client.parser.mango_browser import MangoBrowser
import logging
logging.getLogger('matplotlib').setLevel(logging.INFO)


file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from utils.dict_utils import DictUtils

from client.demo import data_dir

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    votable_path = os.path.join(data_dir,
                                "annotated_data",
                                "vizier_propermotion.annot.xml"
      
                               )
    mango_browser = MangoBrowser(votable_path) 
    mango_parameters = mango_browser.get_parameters()
    DictUtils.print_pretty_json(mango_parameters)

    ra_col = -1
    dec_col = -1
    pmra_col = -1
    pmdec_col = -1
    # Looking for columns having positions and pms
    # Column ranks are the mapped ones, not the native one
    # look at proper_motions to get more
    proper_motions = mango_browser.get_data()
    for cpt in range(len(proper_motions["head"])):
        head = proper_motions["head"][cpt]
        if head.startswith("field:coords:Point.axis1") is True :
            ra_col = cpt
        elif head.startswith("field:coords:Point.axis2") is True :
            dec_col = cpt
        elif head.startswith("field:meas:ProperMotion.lon") is True :
            pmra_col = cpt
        elif head.startswith("field:meas:ProperMotion.lat") is True :
            pmdec_col = cpt
       
    ra = []
    dec = []
    pm_ra = []
    pm_dec = []
    # Positional values are given in HMS, 
    # Let's use Astropy to convert them in degree.
    # And put data in column oriented arrays
    for data_row in proper_motions["data"]:
        c = SkyCoord((data_row[ra_col] + " " + data_row[dec_col]), frame='icrs', unit=(u.hourangle, u.deg))
        ra.append(c.ra.degree)
        dec.append(c.dec.degree)
        pm_ra.append(data_row[pmra_col])
        pm_dec.append(data_row[pmdec_col])

    fig = plt.figure(figsize=(8,6))
    plt.xlabel('ra (deg)')
    plt.ylabel('dec (deg)')
    plt.title("Proper Motion Demo [Positions and Proper Motions - North (Roeser+, 1988)]")
    plt.scatter(ra, dec) 
    plt.quiver(ra, dec, pm_ra, pm_dec, scale=0.5, color="red")
    plt.grid()
    plt.show()
