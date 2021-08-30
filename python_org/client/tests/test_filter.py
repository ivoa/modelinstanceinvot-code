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
        self.assertDictEqual(json.loads(json.dumps(builder.json))
                             , DictUtils.read_dict_from_file(self.json_ref_path)
                             , "=======")
        
    def test_22(self):
        self.maxDiff = None
        if self.populated is False:
            self.vodml_instance.populate_templates()
            self.vodml_instance.connect_join_iterators()
            self.populated = True
        table_mapper = self.vodml_instance.table_mappers["Results"]
        full_dict = table_mapper.get_full_instance()

        #
        print(DictUtils.get_pretty_json(full_dict))
        self.assertDictEqual(full_dict, DictUtils.read_dict_from_file(self.json_ref_path_inst), "")
        
    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_filter.xml")
        self.json_ref_path = os.path.join(self.data_path, "./data/test_filter_1.json")
        self.json_refi_path = os.path.join(self.data_path, "./data/test_filter_2.json")
        self.json_ref_path_inst = os.path.join(self.data_path, "./data/test_filter_instance.json")

        logger.info("processing %s", self.votable_path)
        self.populated = False
        self.vodml_instance = VodmlInstance(self.votable_path)
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
