# coding: utf-8
'''
Created on 30 août 2021

@author: michel
'''
import os, unittest
from utils.file_utils import FileUtils
from utils.dict_utils import DictUtils
from client.translator.mapping_to_json import MappingToJson

class Test(unittest.TestCase):


    def testMappingToJson(self):
        self.maxDiff = None
        mapping_to_json = MappingToJson(os.path.join(FileUtils.get_datadir(), "rich_instance.xml")
                                        ,  exit_validation=False)
        mapping_to_json._extract_vodml_block()
        mapping_to_json._validate_vodml_block()
        DictUtils.print_pretty_json(mapping_to_json.json_block)
        self.assertDictEqual(mapping_to_json.json_block
                             , DictUtils.read_dict_from_file(os.path.join(FileUtils.get_datadir()
                                                                          , "references/rich_instance_raw.json")))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()