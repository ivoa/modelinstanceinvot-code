"""
Created on Jan 6, 2022

@author: laurentmichel
"""
import unittest
import os
from astropy.io.votable import parse

from mivot_code.utils.xml_utils import XmlUtils
from mivot_code.utils.dict_utils import DictUtils
from mivot_code.client.xml_interpreter.model_viewer import ModelViewer
from mivot_code.client.class_wrappers.mango.mango_parameter import MangoObject

class TestLonLatPoint(unittest.TestCase):
    votable = None
    mviewer = None
    def test_global_getters(self):      
        self.maxDiff = None
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['result_S1655295529955'])
        self.mviewer.connect_table(None)
        _ = self.mviewer.get_next_row()       

        #XmlUtils.pretty_print(self.mviewer.get_model_view(resolve_ref=True))
        #DictUtils.print_pretty_json(self.mviewer.get_json_model_view(resolve_ref=False))
        #DictUtils.print_pretty_json(self.mviewer.get_json_model_component_by_type("coords:SpaceFrame"))
        mango_object = None
        for mango_type in self.mviewer.get_model_component_by_type("mango:MangoObject"):
            print("============================")
            mango_object = MangoObject(mango_type)
            break
        
        print(mango_object.identifier)
        for mango_parameter in mango_object._parameters:
            print(f"   {mango_parameter}")
        
        print("\n=== Dataset space frame(s)")
        for mango_parameter in mango_object._parameters:
            if mango_parameter.isPosition():
                print(mango_parameter.measure.coord.coordSys.label)

        print("\n=== Dataset photometric filters(s)")
        for mango_parameter in mango_object._parameters:
            if mango_parameter.isPhotometry():
                print(mango_parameter.measure.coord.coordSys.frame.photCal.photometryFilter)
       

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/xtapdb.pos_hr_flux.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, 
                                      votable_path=os.path.join(
                                        cls.data_path, 
                                        "data/xtapdb.pos_hr_flux.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()