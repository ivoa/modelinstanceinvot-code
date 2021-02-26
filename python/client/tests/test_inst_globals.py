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
        votable_path = os.path.join(data_path, "./data/test_globals.xml")
        json_ref_path = os.path.join(data_path, "./data/test_globals_1.json")
        table_mapper = TableMapper("Results"
                             , votable_path
                             , json_inst_dict=DictUtils.read_dict_from_file(json_ref_path))
        table_mapper.resolve_refs_and_values(resolve_refs=True)

        # print(DictUtils.get_pretty_json(table_mapper.json["MODEL_INSTANCE"]["TABLE_MAPPING"]["my:other.role"]))
        self.assertDictEqual(table_mapper.json["MODEL_INSTANCE"]["TABLE_MAPPING"]["Results"]["my:other.role"]
                             , {
                              "@ID": "TestParamRef",
                              "@dmtype": "Whatever",
                              "coords:whatever": {
                                "@dmtype": "coords:StdRefLocation",
                                "coords:StdRefLocation.position": {
                                  "@dmtype": "ivoa:string",
                                  "@ref": "param_ref",
                                  "@value": "param_value"
                                }
                              }
                            } 
                             , "")
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
