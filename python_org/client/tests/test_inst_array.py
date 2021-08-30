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


class TestInstance(unittest.TestCase):

    def test_1(self):
        self.maxDiff = None
        data_path = os.path.dirname(os.path.realpath(__file__))
        votable_path = os.path.join(data_path, "./data/test_array.xml")
        json_ref_path = os.path.join(data_path, "./data/test_array_1.json")
        table_mapper = TableMapper("Results"
                             , votable_path
                             , json_inst_dict=DictUtils.read_dict_from_file(json_ref_path))
        table_mapper.resolve_refs_and_values()

        self.assertListEqual([*table_mapper.table_iterators], ['meas:Error.statError'], "")
        self.assertDictEqual(table_mapper.table_iterators['meas:Error.statError'].column_mapping.column_refs
                             , {'_poserr_148': {'parent_role': 'meas:Symmetrical.radius', 'role': 'ivoa:RealQuantity.value', 'index': None, 'field': None}}
                             , "")
        
        table_mapper.map_columns()
        self.assertDictEqual(table_mapper.table_iterators['meas:Error.statError'].column_mapping.column_ids
                             , {0: {'name': 'oidsaada', 'ref': None, 'id': '_poserr_148'}}
                             , "")

        self.assertListEqual(table_mapper.get_flatten_data_head()
                         , ['meas:Symmetrical.radius(ivoa:RealQuantity.value) [col#0 _poserr_148]'], ""),
        cpt = 1
        while True:
            inst = table_mapper._get_next_flatten_row()
            if inst != None:
                self.assertListEqual(inst, [cpt], "")
                cpt += 1
            else:
                break
        table_mapper.rewind()
        cpt = 1
        while True:
            inst = table_mapper._get_next_row_instance()
            if inst != None:
                self.assertDictEqual(inst
                                     , {
                                      "@dmtype": "meas:Symmetrical",
                                      "meas:Symmetrical.radius": {
                                        "@dmtype": "ivoa:RealQuantity",
                                        "ivoa:Quantity.unit": {
                                          "@dmtype": "ivoa:Unit",
                                          "@value": "arcsec"
                                        },
                                        "ivoa:RealQuantity.value": {
                                          "@dmtype": "ivoa:real",
                                          "@ref": "_poserr_148",
                                          "@value": cpt
                                        }
                                      }
                                    }
                                     , "")
                cpt += 1
            else:
                break
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
