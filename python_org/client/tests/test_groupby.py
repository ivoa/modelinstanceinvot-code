'''
Created on 22 juin 2020

@author: laurentmichel
'''
import unittest
import os
import json
import sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from client.translator.json_mapping_builder import JsonMappingBuilder
from client.translator.instance_from_votable import InstanceFromVotable
from client.inst_builder.vodml_instance import VodmlInstance
from client.tests import logger
from utils.dict_utils import DictUtils


class TestInstance(unittest.TestCase):

    def test_1(self):
        self.maxDiff = None

        logger.info("extract vodml block from %s", self.votable_path)
        instanceFromVotable = InstanceFromVotable(self.votable_path)
        
        instanceFromVotable._extract_vodml_block()
        instanceFromVotable._validate_vodml_block()
        
        builder = JsonMappingBuilder(json_dict=instanceFromVotable.json_block)
        # builder.revert_array()

        builder.revert_compositions("COLLECTION")
        builder.revert_templates()
        builder.revert_elements("INSTANCE")
        builder.revert_elements("ATTRIBUTE")
        # print(DictUtils.get_pretty_json(builder.json))
        self.assertDictEqual(json.loads(json.dumps(builder.json))
                             , DictUtils.read_dict_from_file(self.json_ref_path)
                             , "test_1 failed")
    
    def test_2(self):
        self.maxDiff = None 
        self.vodml_instance.populate_templates()
        self.vodml_instance.connect_join_iterators()
        self.populated = True
        self.assertDictEqual(json.loads(json.dumps(self.vodml_instance.json_view))
                             , DictUtils.read_dict_from_file(self.json_ref_path_inst)
                             , "test_2 failed")

        table_mapper = self.vodml_instance.table_mappers["Results"]
        # print(DictUtils.get_pretty_json(table_mapper.get_full_instance()))
        retour = {}
        for data_subset in table_mapper.table_iterators.keys():
            table = []

            while True:
                inst = table_mapper._get_next_flatten_row(data_subset=data_subset)
                if inst != None:
                    table.append(inst)
                else:
                    break
            retour[data_subset] = table
        # print(DictUtils.get_pretty_json(retour))
        self.assertDictEqual(retour, DictUtils.read_dict_from_file(self.json_ref_path_data), "")
        
    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_groupby.xml")
        self.json_ref_path = os.path.join(self.data_path, "./data/test_groupby_1.json")
        self.json_ref_path_inst = os.path.join(self.data_path, "./data/test_groupby_instance.json")
        self.json_ref_path_data = os.path.join(self.data_path, "./data/test_groupby_data.json")

        logger.info("processing %s", self.votable_path)
        self.populated = False
        self.vodml_instance = VodmlInstance(self.votable_path)
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
