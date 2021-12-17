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
from client.objectbuilder.vodml_instance2 import VodmlInstance2
from client.objectbuilder.mapping_block_pointer import MappingBlockPointer
from client.objectbuilder.mapping_exception import MappingException

class Test(unittest.TestCase):
    
    def testTableReadout(self):
        
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/mapping_blocks/test.2.1.rich.json")
        
        try :
            MappingBlockPointer.get_globals()
            self.assertTrue(False, " an exception should be risen")
        except MappingException:
            self.assertTrue(True)
            
        MappingBlockPointer.init(DictUtils.read_dict_from_file(self.sample_path))
        Checker.check_dict(MappingBlockPointer.get_globals(), "test.2.1.ok.1.json")

        self.assertEqual(len(MappingBlockPointer.get_templates_blocks()), 2)
        Checker.check_dict(MappingBlockPointer.get_templates("Results"), "test.2.1.ok.2.json")
        try :
            MappingBlockPointer.get_templates("Results_WWWWWWW")
            self.assertTrue(False, " an exception should be risen")
        except MappingException:
            self.assertTrue(True)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
