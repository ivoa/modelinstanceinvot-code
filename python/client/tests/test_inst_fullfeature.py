'''
Created on 22 juin 2020

@author: laurentmichel
'''
import unittest
import os
import sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from client.inst_builder.table_mapper import TableMapper
from utils.dict_utils import DictUtils
from client.translator.instance_from_votable import InstanceFromVotable
from client.translator.json_mapping_builder import JsonMappingBuilder


class TestInstanceFullFeature(unittest.TestCase):

    def test_1(self):
        self.json_ref_path = os.path.join(self.data_path, "./data/test_inst_fullfeature_1.json")
        self.maxDiff = None
        self.table_mapper.resolve_refs_and_values()
        self.table_mapper.map_columns()
        full_dict = self.table_mapper.get_full_instance()
        # print(DictUtils.get_pretty_json(full_dict))
        # print( DictUtils.read_dict_from_file(json_ref_path))
        self.assertDictEqual(full_dict, DictUtils.read_dict_from_file(self.json_ref_path), "")  
              
    def test_2(self):
        self.json_ref_path = os.path.join(self.data_path, "./data/test_inst_fullfeature_2.json")
        self.maxDiff = None
        self.table_mapper.resolve_refs_and_values()
        self.table_mapper.map_columns()
        full_dict = self.table_mapper.get_full_instance(resolve_refs=True)
        # print(DictUtils.get_pretty_json(full_dict))
        # print( DictUtils.read_dict_from_file(json_ref_path))
        self.assertDictEqual(full_dict, DictUtils.read_dict_from_file(self.json_ref_path), "")        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_inst_fullfeature.xml")
        self.json_ref_path = ""

        self.instanceFromVotable = InstanceFromVotable(self.votable_path)
        
        self.instanceFromVotable._extract_vodml_block()
        self.instanceFromVotable._validate_vodml_block()
      
        self.builder = JsonMappingBuilder(json_dict=self.instanceFromVotable.json_block)
        # builder.revert_array()

        self.builder.revert_compositions("COLLECTION")
        self.builder.revert_templates()
        self.builder.revert_elements("INSTANCE")
        self.builder.revert_elements("ATTRIBUTE")
        # print(DictUtils.get_pretty_json(builder.json))
        
        self.table_mapper = TableMapper("Results"
                             , self.votable_path
                             , json_inst_dict=self.builder.json
                                 )

    
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
