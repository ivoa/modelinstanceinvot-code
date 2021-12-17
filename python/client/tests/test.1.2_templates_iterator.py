"""
Created on 1 sept. 2021

@author: michel
"""
import os
import unittest
from collections import OrderedDict
from client.objectbuilder.templates_iterator import TemplatesIterator
from client.objectbuilder.column_mapping import ColumnMapping
from utils.dict_utils import DictUtils
from client.objectbuilder.votable_pointer import  VOTablePointer
from client.tests.checker import Checker

class Test(unittest.TestCase):
    
    def testSimpleJoin(self):
        
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/mapping_blocks/test.1.2.simple_join.json")
        
        VOTablePointer.connect(os.path.join(self.data_path, "./data/votables/multitables.xml"))
        
        json_block = DictUtils.read_dict_from_file(self.sample_path)
                
        templates_iterator = TemplatesIterator("Sources", json_block)
        templates_iterator._map_columns()
        Checker.check_dict(templates_iterator._column_mapping.column_refs, "test.1.2.ok.1.json")

        self.assertEqual(templates_iterator._column_mapping.table_name, "Sources")
 
        row = templates_iterator.get_next_row()
        self.assertListEqual(list(row), ['source1', 'source1_ra', 'source1_dec'])
        row = templates_iterator.get_next_row()
        self.assertListEqual(list(row), ['source2', 'source2_ra', 'source2_dec'])


        templates_iterator._setup_joins()
        templates_iterator.rewind()
        self.assertListEqual(templates_iterator.get_next_flatten_row(), 
                             ['source1', 'source1_ra', 'source1_dec'])
        self.assertListEqual(templates_iterator.get_next_flatten_row(), 
                             ['source2', 'source2_ra', 'source2_dec'])
        self.assertDictEqual( templates_iterator.get_associated_data(), 
            {
              "test.detections": [
                [
                  "detection21",
                  "source2",
                  "detection21_ra",
                  "detection21_dec"
                ],
                [
                  "detection22",
                  "source2",
                  "detection22_ra",
                  "detection22_dec"
                ]
              ]
            })


        self.assertListEqual(
            templates_iterator.get_flatten_data_head(),
            [
                "Point (NOROLE->test:point.id) [col#0 _id (None)]",
                "Point (NOROLE->test:point.ra) [col#1 _ra (None)]",
                "Point (NOROLE->test:point.dec) [col#2 _dec (None)]"
            ]
        )
        
        templates_iterator.rewind()
        next_row_instance = templates_iterator.get_next_row_instance()
        Checker.check_dict(next_row_instance, "test.1.2.ok.2.json")



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
