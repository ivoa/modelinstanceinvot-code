"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from client.tests import logger
from client.translator.json_mapping_builder import JsonMappingBuilder
from client.translator.vocabulary import Att, Ele
from utils.dict_utils import DictUtils
from client.objectbuilder.json_block_extractor import JsonBlockExtractor

class Test(unittest.TestCase):

    def test_search_object_container(self):
        self.maxDiff = None
        self.json_view =DictUtils.read_dict_from_file(
            os.path.join(self.data_path, "./data/mapping_blocks/test.1.2.simple_join.json"))

        json = JsonBlockExtractor.search_object_container(self.json_view, "test.detections")
        DictUtils.print_pretty_json(json)
        self.assertEqual(len(json), 1)

        json = json[0]
        self.assertDictEqual(json
                             ,DictUtils.read_dict_from_file(os.path.join(self.data_path
                                                       , "./data/references/extractor_object_container.json"))
                             )

 
        
    def test_search_by_type(self):
        self.maxDiff = None
        self.json_view =DictUtils.read_dict_from_file(self.json_path)

        json = JsonBlockExtractor.search_subelement_by_type(self.json_view, "test.model")
        self.assertEqual(len(json), 1)

        json = json[0]
        self.assertDictEqual(json
                             ,DictUtils.read_dict_from_file(os.path.join(self.data_path
                                                       , "./data/references/extractor_by_type.raw.json"))
                             )

        JsonBlockExtractor.revert_model_element(json)
        self.assertDictEqual(json
                             ,DictUtils.read_dict_from_file(os.path.join(self.data_path
                                                       , "./data/references/extractor_by_type.revert.json"))
                             )

    def test_search_by_id(self):
        self.maxDiff = None
        self.json_view =DictUtils.read_dict_from_file(self.json_path)

        json = JsonBlockExtractor.search_subelement_by_id(self.json_view, "_point")

        self.assertEqual(len(json), 1)

        json = json[0]
        self.assertDictEqual(json
                             ,DictUtils.read_dict_from_file(os.path.join(self.data_path
                                                       , "./data/references/extractor_by_id.raw.json"))
                             )

        JsonBlockExtractor.revert_model_element(json)
        self.assertDictEqual(json
                             ,DictUtils.read_dict_from_file(os.path.join(self.data_path
                                                       , "./data/references/extractor_by_id.revert.json"))
                             )

    def test_search_joins(self):
        self.maxDiff = None
        
        self.json_view =DictUtils.read_dict_from_file(self.json_path)
        
        json = JsonBlockExtractor.search_subelement_by_type(self.json_view, "test.model")
        
        JsonBlockExtractor.revert_model_element(json)
        json = JsonBlockExtractor.search_join_container(json)
        self.assertDictEqual(json,
                {
                  "test.points": {
                    "dm-mapping:JOIN": {
                      "@dmref": "_point",
                      "@tableref": "Results"
                    }
                  }
                }                             
                )



    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/references/test_json_block_extractor.input.1.json")
        self.json_view =DictUtils.read_dict_from_file(self.json_path)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()