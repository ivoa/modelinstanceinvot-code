"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from lxml import etree

from client.tests import logger
from client.translator.json_mapping_builder import JsonMappingBuilder
from client.translator.vocabulary import Att, Ele
from utils.dict_utils import DictUtils
from client.translator.mapping_to_json import MappingToJson
from client.objectbuilder.mapping_block_cursor import MappingBlockCursor

class TestMapppingBuilder(unittest.TestCase):

    def test_all_reverts(self):        
        
        tree = etree.parse(os.path.join(self.data_path, "data/mapping_blocks/test.0.1.TS.xml"))
        root = tree.getroot()
        etree.cleanup_namespaces(tree)
        #ßprint(etree.tostring(tree, pretty_print=True).decode("utf-8"))
        MappingBlockCursor.init(root)
        #print(etree.tostring(tree, pretty_print=True).decode("utf-8"))
        MappingBlockCursor.get_json_block()
        #DictUtils.print_pretty_json(MappingBlockCursor.get_json_block())

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/mapping_blocks/test.3.1.rich.json")
        self.revert_json_path = os.path.join(self.data_path, "./data/references/rich_instance_revert.json")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()