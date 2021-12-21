"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from utils.dict_utils import DictUtils
from client.xml_interpreter.top_level_collection import TopLevelCollection
from client.xml_interpreter.to_json_converter import ToJsonConverter
class TestToJsonConverter(unittest.TestCase):

 

  
    def test_results(self):      
        tlc = TopLevelCollection(os.path.join(self.data_path, "data/input/test.1.xml"))
        tlc.connect_table('Results')
        tlc._squash_join_and_references()
        tlc._set_column_indices()
        tlc.get_next_row()
        tjc = ToJsonConverter(tlc.get_model_view())
        
        tjc._translate_xml()
        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.1.json"
                )
            ),
        )


        tjc._revert_collections()
        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.2.json"
                )
            ),
        )


        tjc._revert_attributes()
        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.3.json"
                )
            ),
        )

        tjc._revert_instances()
        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.4.json"
                )
            ),
        )
        
        self.assertListEqual(
            tjc.get_json_instance(),
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.5.json"
                )
            ),
        )
 

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()