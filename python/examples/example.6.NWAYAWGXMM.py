"""
Created on Jan 6, 2022

@author: laurentmichel
"""
import unittest
import os
from astropy.io.votable import parse

from utils.xml_utils import XmlUtils
from utils.dict_utils import DictUtils
from client.xml_interpreter.model_viewer import ModelViewer

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
    for phot_point in phot_points:
        XmlUtils.pretty_print(phot_point)
    break
