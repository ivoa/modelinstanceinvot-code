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
        self.mviewer.connect_table(None)
        
        print("Reading Mango objects:")

        while self.mviewer.get_next_row()   is not None:
            for mango_type in self.mviewer.get_model_component_by_type("mango:MangoObject"):
                mango_object = MangoObject(mango_type)
                for mango_parameter in mango_object._parameters:
                    print(f"{mango_object.identifier}:  {mango_parameter}")

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/xtapdb.status.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, 
                                      votable_path=os.path.join(
                                        cls.data_path, 
                                        "data/xtapdb.status.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()