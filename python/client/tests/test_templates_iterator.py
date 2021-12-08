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

class Test(unittest.TestCase):
    
    def testJoins(self):
        
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/references/test_templates_iterator.input.2.json")
        
        VOTablePointer.connect(os.path.join(self.data_path, "./data/rich_instance.xml"))
        
        json_block = DictUtils.read_dict_from_file(self.sample_path)
                
        templates_iterator = TemplatesIterator("Results", json_block)
        templates_iterator._map_columns()

        self.assertDictEqual(templates_iterator._column_mapping.column_refs,
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
        
        self.assertEqual(templates_iterator._column_mapping.table_name, "Results")
 
        row = templates_iterator.get_next_row()
        self.assertEqual(row[0], 1)

        row = templates_iterator.get_next_row()
        self.assertEqual(row[0], 2)
        templates_iterator.rewind()
        templates_iterator._setup_joins()
        self.assertListEqual(list(templates_iterator._joined_templates.keys()), ['OtherResults', 'Spectra'])
        self.assertListEqual( templates_iterator.get_next_flatten_row(), [1])
        self.assertDictEqual( templates_iterator.get_associated_data(), 
                {
                  "OtherResults": [
                    [
                      1, 11
                    ],
                    [
                      1,  12
                    ]
                  ],
                  "Spectra": [
                    [
                      1, "Spectrum 11"
                    ],
                    [
                      1, "Spectrum 12"
                    ]
                  ]
                })
        self.assertTrue(False)
        templates_iterator.rewind()
        self.assertListEqual(templates_iterator.get_next_flatten_row(), [1])
        self.assertListEqual(templates_iterator.get_next_flatten_row(), [2])

        templates_iterator.rewind()
        
        next_row_instance = templates_iterator.get_next_row_instance()
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
        next_row_instance = templates_iterator.get_next_row_instance()
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
            templates_iterator.get_flatten_data_head(),
            ['test:Spectrum (NOROLE->test:spectrum.id) [col#1 _foreign_spectra (meta.id;meta.main)]',
             'test:Spectrum (NOROLE->test:spectrum.num) [col#0 _spc_148 (meta.id;meta.main)]'],
        )
    """
    def testSimple(self):
        
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/references/test_templates_iterator.input.1.json")
        
        VOTablePointer.connect(os.path.join(self.data_path, "./data/rich_instance.xml"))
        
        json_block = DictUtils.read_dict_from_file(self.sample_path)
                
        templates_iterator = TemplatesIterator(json_block)
        templates_iterator._map_columns()
        self.assertDictEqual(templates_iterator._column_mapping.column_refs
                             , DictUtils.read_dict_from_file(
                                 os.path.join(self.data_path, 
                                              "./data/references/test_templates_iterator.output.1.json")))
        
        self.assertEqual(templates_iterator._column_mapping.table_name, "Spectra")
 
        row = templates_iterator.get_next_row()
        self.assertEqual(row[0], "Spectrum 11")
        self.assertEqual(row[1], 1)

        row = templates_iterator.get_next_row()
        self.assertEqual(row[0], "Spectrum 12")
        self.assertEqual(row[1], 1)

        templates_iterator.rewind()
        self.assertListEqual(templates_iterator.get_next_flatten_row(), [1, 'Spectrum 11'])
        self.assertListEqual(templates_iterator.get_next_flatten_row(), [1, 'Spectrum 12'])

        templates_iterator.rewind()
        
        next_row_instance = templates_iterator.get_next_row_instance()
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
        next_row_instance = templates_iterator.get_next_row_instance()
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
            templates_iterator.get_flatten_data_head(),
            ['test:Spectrum (NOROLE->test:spectrum.id) [col#1 _foreign_spectra (meta.id;meta.main)]',
             'test:Spectrum (NOROLE->test:spectrum.num) [col#0 _spc_148 (meta.id;meta.main)]'],
        )
    """

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
