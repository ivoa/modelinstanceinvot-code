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


class TestMapppingBuilder(unittest.TestCase):

    def test_all_reverts(self):
        self.maxDiff = None
        builder = JsonMappingBuilder(
            json_dict=DictUtils.read_dict_from_file(self.json_path)
        )
        
        
        builder.revert_collections()
        DictUtils.print_pretty_json(builder.json)
        self.assertDictEqual(
            builder.json,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "./data/references/rich_instance_revert_coll.json"
                )
            ),
        )

        builder.revert_templates()
        self.assertDictEqual(
            builder.json,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "./data/references/rich_instance_revert_templ.json"
                )
            ),
        )

        builder.revert_elements("dm-mapping:INSTANCE")
        self.assertDictEqual(
            builder.json,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "./data/references/rich_instance_revert_inst.json"
                )
            ),
        )

        builder.revert_elements("dm-mapping:ATTRIBUTE")
        self.assertDictEqual(
            builder.json, DictUtils.read_dict_from_file(self.revert_json_path)
        )


    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/mapping_blocks/test.3.1.rich.json")
        self.revert_json_path = os.path.join(self.data_path, "./data/references/rich_instance_revert.json")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()