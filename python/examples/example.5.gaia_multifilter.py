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
votable = parse(os.path.join(data_path, "gaia_multifilters.xml"))
for resource in votable.resources:
    mviewer = ModelViewer(resource, votable_path=os.path.join(data_path, "gaia_multifilters.xml"))
    break;

XmlUtils.pretty_print(mviewer.get_globals_instance("cube:SparseCube")[0])
DictUtils.print_pretty_json(mviewer.get_globals_instance_json_model_view("cube:SparseCube")[0])