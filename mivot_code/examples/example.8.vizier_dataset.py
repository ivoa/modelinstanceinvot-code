"""
Created on Nov 2, 2022

@author: laurentmichel
"""
import unittest
import os
from astropy.io.votable import parse

from mivot_code.utils.xml_utils import XmlUtils
from mivot_code.utils.dict_utils import DictUtils
from mivot_code.client.xml_interpreter.model_viewer import ModelViewer

class TestLonLatPoint(unittest.TestCase):
    votable = None
    mviewer = None
    def test_global_getters(self):      
        self.maxDiff = None
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['result_S1667130446374'])
        self.mviewer.connect_table('result_S1667130446374')
        
        globals_models = self.mviewer.get_globals_models()
        DictUtils.print_pretty_json(globals_models)
        for dataset in self.mviewer.get_globals_instance(globals_models["COLLECTION"][0]):
            XmlUtils.pretty_print(dataset)
            XmlUtils.pretty_print(XmlUtils.get_attribute_by_role(dataset, "dataset:DataID.datasetDID"))
            print(XmlUtils.get_attribute_by_role(dataset, "dataset:DataID.datasetDID").get("value"))
        
    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/vizier_dataset.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "data/vizier_dataset.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()