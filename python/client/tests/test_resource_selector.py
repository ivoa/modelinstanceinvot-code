# coding: utf-8
'''
Created on 30 août 2021

@author: michel
'''
import os, unittest
from utils.file_utils import FileUtils
from utils.dict_utils import DictUtils
from client.translator.resource_selector import ResourceSelector

class Test(unittest.TestCase):


    def testMappingToJson(self):
        resource_selector = ResourceSelector(os.path.join(FileUtils.get_datadir(), "rich_instance.xml"))
        resource_selector.validate()
        self.assertTrue(resource_selector.is_valid)
        self.assertTrue(resource_selector.is_mapped)
        resource_selector.map_table()
        self.assertListEqual(list(resource_selector.tables.keys()), ['Results', 'OtherResults', 'Spectra'])
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()