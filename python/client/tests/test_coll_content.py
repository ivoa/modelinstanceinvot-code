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

from client.translator.json_mapping_builder import JsonMappingBuilder
from client.translator.instance_from_votable import InstanceFromVotable
from client.tests import logger
from utils.dict_utils import DictUtils


class TestInstance(unittest.TestCase):

    def test_1(self):
        self.maxDiff = None
        data_path = os.path.dirname(os.path.realpath(__file__))
        votable_path = os.path.join(data_path, "./data/test_coll_content1.xml")
        json_ref_path = os.path.join(data_path, "./data/test_coll_content1.json")
        logger.info("extract vodml block from %s", votable_path)
        instanceFromVotable = InstanceFromVotable(votable_path)
        
        instanceFromVotable._extract_vodml_block()
        instanceFromVotable._validate_vodml_block()
        
        builder = JsonMappingBuilder(json_dict=instanceFromVotable.json_block)
        builder.revert_compositions("COLLECTION")
        builder.revert_compositions("INSTANCE")

        print(DictUtils.get_pretty_json(builder.json["MODEL_INSTANCE"]["TABLE_MAPPING"]))
        self.assertDictEqual(builder.json["MODEL_INSTANCE"]["TABLE_MAPPING"], DictUtils.read_dict_from_file(json_ref_path), "=======")
        
    def test_2(self):
        self.maxDiff = None
        data_path = os.path.dirname(os.path.realpath(__file__))
        votable_path = os.path.join(data_path, "./data/test_coll_content2.xml")
        json_ref_path = os.path.join(data_path, "./data/test_coll_content2.json")
        logger.info("extract vodml block from %s", votable_path)
        instanceFromVotable = InstanceFromVotable(votable_path)
        
        instanceFromVotable._extract_vodml_block()
        instanceFromVotable._validate_vodml_block()
        
        builder = JsonMappingBuilder(json_dict=instanceFromVotable.json_block)
        builder.revert_compositions("COLLECTION")
        builder.revert_compositions("INSTANCE")

        print(DictUtils.get_pretty_json(builder.json["MODEL_INSTANCE"]["TABLE_MAPPING"]))
        self.assertDictEqual(builder.json["MODEL_INSTANCE"]["TABLE_MAPPING"], DictUtils.read_dict_from_file(json_ref_path), "=======")

    def test_3(self):
        self.maxDiff = None
        data_path = os.path.dirname(os.path.realpath(__file__))
        votable_path = os.path.join(data_path, "./data/test_coll_content3.xml")
        json_ref_path = os.path.join(data_path, "./data/test_coll_content3.json")
        logger.info("extract vodml block from %s", votable_path)
        instanceFromVotable = InstanceFromVotable(votable_path)
        
        instanceFromVotable._extract_vodml_block()
        instanceFromVotable._validate_vodml_block()
        
        builder = JsonMappingBuilder(json_dict=instanceFromVotable.json_block)
        builder.revert_compositions("COLLECTION")
        builder.revert_compositions("INSTANCE")

        print(DictUtils.get_pretty_json(builder.json["MODEL_INSTANCE"]["TABLE_MAPPING"]))
        self.assertDictEqual(builder.json["MODEL_INSTANCE"]["TABLE_MAPPING"], DictUtils.read_dict_from_file(json_ref_path), "=======")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
