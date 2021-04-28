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
    votable_paths = [
        
        os.path.join(data_dir,
            "annotated_data",
            "NGC5139_4xmm.annot.xml"
            ),
        os.path.join(data_dir,
            "annotated_data",
            "NGC5139_gaiadr2.annot.xml"
            ),
        os.path.join(data_dir,
            "annotated_data",
            "ivoa_csc2_example.annot.xml"
            )
        ]
    
    layouts = {
        0: {
            "marker": "x",
            "color": "red",
            "label": "4xmm",
            "size": 40,
            "plot": None
            },
        1: {
            "marker": "o",
            "color": "blue",
            "label": "gaia dr2",
            "size": 1,
            "plot": None
            },
        2: {
            "marker": "x",
            "color": "green",
            "label": "Chandra",
            "size": 40,
            "plot": None
            },
        }
        
    fig = plt.figure(figsize=(8,6))
    plt.xlabel('ra (deg)')
    plt.ylabel('dec (deg)')
    plt.title("NCG5139 Demo")
    color = "red"

    target = SkyCoord("13:26:45.89 -47:28:36.7", unit=(u.hour, u.deg))
    box_halfsize = 0.03
    plan = 0
    for votable_path in votable_paths:
        mango_browser = MangoBrowser(votable_path) 
        mango_parameters = mango_browser.get_parameters()

        if "#1 pos.eq" in mango_parameters:
            mango_parameter = mango_parameters["#1 pos.eq"]
        if "#1 pos" in mango_parameters:
            mango_parameter = mango_parameters["#1 pos"]
            
        mango_frame  = mango_parameter[mango_parameter["coosys_type"]]
        frame = mango_frame["coords:SpaceFrame.spaceRefFrame"]["@value"].lower()
    
        position_data = mango_browser.get_data(measure_type="mango:stcextend.LonLatSkyPosition")
    
        ra_col = -1
        dec_col = -1
        # Looking for columns having positions a
        # Column ranks are the mapped ones, not the native one
        for cpt in range(len(position_data["head"])):
            head = position_data["head"][cpt]
            if head.startswith("field:longitude") is True :
                ra_col = cpt
            elif head.startswith("field:latitude") is True :
                dec_col = cpt
           
        ra = []
        dec = []
        # Positional values are given in HMS, 
        # Let's use Astropy to convert them in degree.
        for data_row in position_data["data"]:
            c = SkyCoord(data_row[ra_col], data_row[dec_col], frame=frame, unit=(u.deg, u.deg))
            rap = c.icrs.ra.degree
            decp = c.icrs.dec.degree
            if (rap > (target.ra.degree - box_halfsize) and rap < (target.ra.degree + box_halfsize) 
                and decp > (target.dec.degree - box_halfsize) and decp < (target.dec.degree + box_halfsize)):
                ra.append(rap)
                dec.append(decp)
    
        layout = layouts[plan]
        layout["plot"] = plt.scatter(ra, dec, color=layout["color"], marker=layout["marker"], s=layout["size"])
        
        plan += 1
        if color == "blue":
            color="green"
        if color == "red":
            color="blue"
            
    plt.legend(
        (layouts[0]["plot"], layouts[1]["plot"], layouts[2]["plot"]),
        (layouts[0]["label"], layouts[1]["label"], layouts[2]["label"]),
           scatterpoints=1,
           loc='lower left',
           ncol=3,
           fontsize=8)
    print(target)
    print(target.ra.degree)
    print(target.dec.degree)
    plt.gca().invert_xaxis()       
    plt.grid()
    plt.show()
    
