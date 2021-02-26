'''
Created on Feb 26, 2021

@author: laurentmichel
'''
import unittest
import os
from client.tests import logger
from client.translator.json_mapping_builder import JsonMappingBuilder
from utils.dict_utils import DictUtils

class Test(unittest.TestCase):


    def test_revert_templates(self):
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {
                    }
                    }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder.revert_templates()
        self.assertDictEqual(jsonMappingBuilder.json, 
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": {
                  "Results": [
                    {
                      "@tableref": "Results",
                      "COLLECTION": {}
                    }
                  ]
                }
              }
            }
                             )
        print(DictUtils.get_pretty_json(jsonMappingBuilder.json))


    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_json_mapping_builder.json")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()