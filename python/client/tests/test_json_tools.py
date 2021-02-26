'''
Created on 22 juin 2020

@author: laurentmichel
'''
import unittest
import os
import json 
import sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from client.translator.json_tools import JsonTools
from client.tests import logger
from utils.dict_utils import DictUtils


class TestArray(unittest.TestCase):

    def test_1(self):
        self.maxDiff = None
        
        dico = {"INSTANCE": {"A": "a", "B": "b"}}
        retour = JsonTools.remove_key(dico, "INSTANCE")

        # print(DictUtils.get_pretty_json(dico))
        self.assertDictEqual(retour
                             , {'A': 'a', 'B': 'b'}
                             , "=======")

    def test_2(self):
        self.maxDiff = None
        
        dico = {"INSTANCE": [{"A1": "a", "B1": "b"}, {"A2": "a", "B2": "b"}]}
        retour = JsonTools.remove_key(dico, "INSTANCE")

        # print(DictUtils.get_pretty_json(dico))
        self.assertListEqual(retour
                             , [{"A1": "a", "B1": "b"}, {"A2": "a", "B2": "b"}]
                             , "=======")
 
    def test_3(self):
        self.maxDiff = None
        
        dico = [{"INSTANCE": {"A1": "a", "B1": "b"}}]
        retour = JsonTools.remove_key(dico, "INSTANCE")

        # print(DictUtils.get_pretty_json(dico))
        self.assertListEqual(retour
                             , [{"A1": "a", "B1": "b"}]
                             , "=======")
 
    def test_4(self):
        self.maxDiff = None
        
        dico = [{"INSTANCE": [{"A1": "a", "B1": "b"}, {"A2": "a", "B2": "b"}]}]
        retour = JsonTools.remove_key(dico, "INSTANCE")

        # print(DictUtils.get_pretty_json(dico))
        self.assertListEqual(retour
                             , [{"A1": "a", "B1": "b"}, {"A2": "a", "B2": "b"}]
                             , "=======")
       

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
