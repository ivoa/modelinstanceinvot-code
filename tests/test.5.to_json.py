"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from mivot_code.utils.xml_utils import XmlUtils
from mivot_code.client.xml_interpreter.to_json_converter import ToJsonConverter
from mivot_code.utils.dict_utils import DictUtils
class TestTopJson(unittest.TestCase):

    def test_subset(self):      
        self.maxDiff = None
        
        mapping_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.5.1.xml"))  
        
        tjc = ToJsonConverter(mapping_block)
        tjc._translate_xml_templates()
        self.assertDictEqual(tjc.json_instance, 
                             DictUtils.read_dict_from_file(
                                 os.path.join(self.data_path, "data/output/test.5.5.json")))
        tjc._revert_collections()
        self.assertDictEqual(tjc.json_instance, 
                             DictUtils.read_dict_from_file(
                                 os.path.join(self.data_path, "data/output/test.5.1.json")))
        tjc._revert_attributes()
        self.assertDictEqual(tjc.json_instance, 
                             DictUtils.read_dict_from_file(
                                 os.path.join(self.data_path, "data/output/test.5.2.json")))
        tjc._revert_instances()
        self.assertDictEqual(tjc.json_instance, 
                             DictUtils.read_dict_from_file(
                                 os.path.join(self.data_path, "data/output/test.5.3.json")))
     
    def test_all(self):      
        self.maxDiff = None
        
        mapping_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.5.xml"))  
        
        
        tjc = ToJsonConverter(mapping_block)
        json_instance = tjc.get_json_instance()
        self.assertListEqual(json_instance, DictUtils.read_dict_from_file(os.path.join(self.data_path, "data/output/test.5.4.json")))
     

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()