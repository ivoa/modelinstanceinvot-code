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
from client.mango.mango_parameter import MangoObject

class TestLonLatPoint(unittest.TestCase):
    votable = None
    mviewer = None
    def test_global_getters(self):      
        self.maxDiff = None
        print(self.mviewer.get_table_ids())
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['result_S1654263430384'])
        self.mviewer.connect_table(None)
        row = self.mviewer.get_next_row()       

        #XmlUtils.pretty_print(self.mviewer.get_model_view(resolve_ref=True))
        #DictUtils.print_pretty_json(self.mviewer.get_json_model_view(resolve_ref=False))
        #DictUtils.print_pretty_json(self.mviewer.get_json_model_component_by_type("coords:SpaceFrame"))
        mango_object = None
        for position in self.mviewer.get_model_component_by_type("mango:MangoObject"):
            print("============================")
            mango_object = MangoObject(position)
            break
        #print(self.mviewer.get_stc_positions())
        #print(self.mviewer.get_stc_measures())
        print(mango_object.identifier)
        print(mango_object.get_parameter_by_ucd("src.var"))
        measure = mango_object.get_parameter_by_ucd("src.var").measure
        print(measure.type)
    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/xtapdb.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "data/xtapdb.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()