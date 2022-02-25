"""
Created on Jan 6, 2022

@author: laurentmichel
"""
import os
import numpy as np
import logging
import matplotlib
import mplcursors
import matplotlib.pyplot as plt 
from astropy.io.votable import parse
from astropy import units as u
from client.photdm.photcal import PhotCal

from client.xml_interpreter.model_viewer import ModelViewer

matplotlib.font_manager: logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
matplotlib.font_manager: logging.getLogger('matplotlib.ticker').setLevel(logging.WARNING)

data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
votable = parse(os.path.join(data_path, "NWAYAWGXMM.xml"))
for resource in votable.resources:
    mviewer = ModelViewer(resource, votable_path=os.path.join(data_path, "NWAYAWGXMM.xml"))
    break;

mviewer.connect_table(None)
times = []
ras = []
decs = []
while True:
    row = mviewer.get_next_row() 
    print("coucuo")
    if row is None:
        break  
    row_model_view = mviewer.get_model_view(resolve_ref=False)
    """
    NOT FORGET to restore resolve_ref=True
    """
    phot_points = mviewer.get_model_component_by_type("sed:PhotPoint")
    wl = []
    flx = []
    tlt = []
    name = None
    for ele in row_model_view.xpath('.//ATTRIBUTE[@dmrole="sed:Source.name"]'):
        name  = ele.get("value")
        break
    for phot_point in phot_points:
        #XmlUtils.pretty_print(phot_point)
        flux = None
        unit = None
        unit_org = None
        phot_cal = None
        flux_erg = None
        for ele in phot_point.xpath('.//ATTRIBUTE[@dmrole="sed:PhotPoint.flux"]'):
            #XmlUtils.pretty_print(ele)
            try:
                flux = float(ele.get("value"))
                unit_org = ele.get("unit_org")
                unit = ele.get("unit")
            except:
                pass
            break
        for ele in phot_point.xpath('.//INSTANCE[@dmrole="sed:PhotPoint.photcal"]'):
            #XmlUtils.pretty_print(ele)
            phot_cal = PhotCal(ele)
            spec_loc = phot_cal.photometryFilter.spectralLocation
            spec_loc_value = None
            # convert XMM energy into wavelength
            if spec_loc.unitexpression == "keV":
                spec_loc_value = (spec_loc.value * u.keV).to(u.angstrom, equivalencies=u.spectral()).value
            else: 
                spec_loc_value = spec_loc.value
            break
        if flux is not None:
            if unit_org == "mag":
                zeroPoint = phot_cal.zeroPoint.flux.value
                refMag = phot_cal.zeroPoint.referenceMagnitudeValue
                flux_erg = 1e-23 * zeroPoint * np.power( 10, - (flux - refMag)/2.5) * (299792458 / (spec_loc_value*1E-10))
            else:
                flux_erg = flux
            flx.append(flux_erg)
            wl.append(spec_loc_value)
            tlt.append(phot_cal.identifier)
            print(f"{phot_cal.identifier} {spec_loc.value} {spec_loc.unitexpression} {flux_erg}  {unit}")
    
    print(wl)
    print(flx)


    plt.scatter(wl, flx)
    plt.title("Source " + name)
    plt.xscale("log")
    # Lim must be force to wirk on Linux 3.6
    plt.ylim([min(flx)/10, max(flx)*10])
    plt.yscale("log")
    plt.xlabel("Wavelength (angstrom)")
    plt.ylabel("flux (erg/cm2/sec)")
    mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(tlt[sel.index]))
    plt.subplots_adjust(bottom=.15, left=.15) 
    plt.show()


        
