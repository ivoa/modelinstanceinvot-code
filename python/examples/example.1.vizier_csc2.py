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

class TestLonLatPoint(unittest.TestCase):
    votable = None
    mviewer = None
    def test_global_getters(self):      
        self.maxDiff = None
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['Results'])
        self.mviewer.connect_table('Results')
        row = self.mviewer.get_next_row()       

        print(row)
        XmlUtils.pretty_print(self.mviewer.get_model_view(resolve_ref=False))
        DictUtils.print_pretty_json(self.mviewer.get_json_model_view(resolve_ref=False))
        DictUtils.print_pretty_json(self.mviewer.get_json_model_component_by_type("coords:SpaceFrame"))
        for position in self.mviewer.get_model_component_by_type("meas:Position"):
            XmlUtils.pretty_print(position)
        print(self.mviewer.get_stc_positions())
        print(self.mviewer.get_stc_measures())
        
    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/vizier_csc2_gal.annot.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "data/vizier_csc2_gal.annot.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()