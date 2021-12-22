"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from utils.xml_utils import XmlUtils
from utils.dict_utils import DictUtils
from client.xml_interpreter.top_level_collection import TopLevelCollection
from client.xml_interpreter.dynamic_reference import DynamicReference

class TestMapppingBuilder(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        
        tlc = TopLevelCollection(os.path.join(self.data_path, "data/input/test.3.xml"))        
        tlc.connect_table('_PKTable')
        tlc._squash_join_and_references()

        dynamic_ref = DynamicReference("REFERENCE_2", '_PKTable', tlc.references["REFERENCE_2"])
        dynamic_ref._set_mode()
        
        self.assertEqual(dynamic_ref.target_id, '_Datasets')
        self.assertEqual(dynamic_ref.fk_ref, '_pksrcid')
        self.assertEqual(dynamic_ref.fk_col, 0)
        
        row = tlc.get_next_row()    
        XmlUtils.pretty_print(dynamic_ref.get_target_instance(row))
 
        XmlUtils.assertXmltreeEqualsFile(dynamic_ref.get_target_instance(row),
                                         os.path.join(self.data_path, "data/output/test.3.1.xml"))

        
        
 
 

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()