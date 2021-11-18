"""
Created on 1 sept. 2021

@author: michel
"""
import os
import unittest
from utils.dict_utils import DictUtils
from client.objectbuilder.vodml_instance2 import VodmlInstance2


class Test(unittest.TestCase):
    def testName(self):
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/rich_instance.xml")
        vodml_instance = VodmlInstance2(self.json_path)
        vodml_instance.proto_get_head_block("test.model")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
