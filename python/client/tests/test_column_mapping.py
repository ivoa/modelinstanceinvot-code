'''
Created on 1 sept. 2021

@author: michel
'''
import os
import unittest
from client.objectbuilder.vodml_instance import VodmlInstance
from client.objectbuilder.table_mapper import TableMapper
from client.objectbuilder.column_mapping import ColumnMapping
from astropy.io.votable import parse
from client.objectbuilder.votable_pointer import VOTablePointer

from astropy.io.votable import parse
from utils.dict_utils import DictUtils


class Test(unittest.TestCase):


    def testSimple(self):
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/references/test_column.input.1.json")
        json_block = DictUtils.read_dict_from_file(self.sample_path)
        
        column_mapping = ColumnMapping(json_block)
        self.assertDictEqual(column_mapping.column_refs
                             , DictUtils.read_dict_from_file(
                                 os.path.join(self.data_path, 
                                              "./data/references/test_column.output.1.json")))
        
        self.assertEqual(column_mapping.table_name, "Spectra")
        
        VOTablePointer.connect(os.path.join(self.data_path, "./data/rich_instance.xml"))
        ref_path = os.path.join(self.data_path, "./data/references/test_column.output.2.json")
        column_mapping._map_columns()
        self.assertDictEqual(column_mapping.column_refs
                             , DictUtils.read_dict_from_file(ref_path)[0])

        self.assertDictEqual(column_mapping.column_ids[0]
                             , DictUtils.read_dict_from_file(ref_path)[1]["0"])
        self.assertDictEqual(column_mapping.column_ids[1]
                             , DictUtils.read_dict_from_file(ref_path)[1]["1"])
    def testJoins(self):
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/references/test_column.input.2.json")
        json_block = DictUtils.read_dict_from_file(self.sample_path)
        
        column_mapping = ColumnMapping(json_block)
        self.assertDictEqual(column_mapping.column_refs,
            {
              "_poserr_148": {
                "field": None,
                "index": None,
                "parent_role": "NOROLE",
                "parent_type": "Point",
                "role": "test:detection.num",
                "ucd": None
              }
            })
        
        self.assertEqual(column_mapping.table_name, "Results")
        
        VOTablePointer.connect(os.path.join(self.data_path, "./data/rich_instance.xml"))
        column_mapping._map_columns()

        self.assertDictEqual(column_mapping.column_refs,
            {
              "_poserr_148": {
                "field": "<FIELD ID=\"_poserr_148\" datatype=\"long\" name=\"oidsaada\" ucd=\"meta.id;meta.main\"/>",
                "index": 0,
                "parent_role": "NOROLE",
                "parent_type": "Point",
                "role": "test:detection.num",
                "ucd": "meta.id;meta.main"
              }
            })

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()