"""
Created on 1 sept. 2021

@author: michel
"""
import os
import unittest
from collections import OrderedDict

from client.objectbuilder.table_iterator import TableIterator
from client.objectbuilder.column_mapping import ColumnMapping
from utils.dict_utils import DictUtils
from client.objectbuilder.votable_pointer import  VOTablePointer

class Test(unittest.TestCase):
    def testName(self):
        
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/references/test_table_iterator.input.1.json")
        json_block = DictUtils.read_dict_from_file(self.sample_path)
        
        column_mapping = ColumnMapping(json_block)
        self.assertDictEqual(column_mapping.column_refs
                             , DictUtils.read_dict_from_file(
                                 os.path.join(self.data_path, 
                                              "./data/references/test_table_iterator.output.1.json")))
        
        self.assertEqual(column_mapping.table_name, "Spectra")
 
        VOTablePointer.connect(os.path.join(self.data_path, "./data/rich_instance.xml"))
        column_mapping._map_columns()
 

        table_iterator = TableIterator(
            "iterator_key",
            VOTablePointer.get_table(column_mapping.table_name).to_table(),
            {
                "@tableref": "Spectra",
                "NOROLE": {
                  "@dmtype": "test:Spectrum",
                  "test:spectrum.id": {
                    "@dmtype": "ivoa:real",
                    "@ref": "_foreign_spectra",
                    "@value": ""
                  },
                  "test:spectrum.num": {
                    "@dmtype": "ivoa:stringl",
                    "@ref": "_spc_148",
                    "@value": ""
                  }
                }
            },
            column_mapping,
            row_filter=None,
        )
        row = table_iterator._get_next_row()
        self.assertEqual(row[0], "Spectrum 11")
        self.assertEqual(row[1], 1)
        row = table_iterator._get_next_row()
        self.assertEqual(row[0], "Spectrum 12")
        self.assertEqual(row[1], 1)

        table_iterator._rewind()
        self.assertListEqual(table_iterator._get_next_flatten_row(), [1, 'Spectrum 11'])
        self.assertListEqual(table_iterator._get_next_flatten_row(), [1, 'Spectrum 12'])

        table_iterator._rewind()
        
        next_row_instance = table_iterator._get_next_row_instance()
        DictUtils.print_pretty_json(next_row_instance)
        self.assertDictEqual(
            next_row_instance,
            {
              "@tableref": "Spectra",
              "NOROLE": {
                "@dmtype": "test:Spectrum",
                "test:spectrum.id": {
                  "@dmtype": "ivoa:real",
                  "@ref": "_foreign_spectra",
                  "@value": 1
                },
                "test:spectrum.num": {
                  "@dmtype": "ivoa:stringl",
                  "@ref": "_spc_148",
                  "@value": "Spectrum 11"
                }
              }
            },
        )
        next_row_instance = table_iterator._get_next_row_instance()
        self.assertDictEqual(
            next_row_instance,
            {
              "@tableref": "Spectra",
              "NOROLE": {
                "@dmtype": "test:Spectrum",
                "test:spectrum.id": {
                  "@dmtype": "ivoa:real",
                  "@ref": "_foreign_spectra",
                  "@value": 1
                },
                "test:spectrum.num": {
                  "@dmtype": "ivoa:stringl",
                  "@ref": "_spc_148",
                  "@value": "Spectrum 12"
                }
              }
            },
        )

        self.assertListEqual(
            table_iterator._get_flatten_data_head(),
            ['test:Spectrum (NOROLE->test:spectrum.id) [col#1 _foreign_spectra (meta.id;meta.main)]',
             'test:Spectrum (NOROLE->test:spectrum.num) [col#0 _spc_148 (meta.id;meta.main)]'],
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
