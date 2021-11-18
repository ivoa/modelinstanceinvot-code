"""
Created on 8 sept. 2021

@author: michel
"""
import os, unittest
from astropy.io.votable import parse

from client.objectbuilder.join_iterator import JoinIterator
from utils.dict_utils import DictUtils

class Test(unittest.TestCase):
    
    def test_simple(self):
        self.maxDiff = None
        
        join_statement = {
        "dm-mapping:JOIN": {
          "@dmref": "_point",
          "@tableref": "Results"
        }
        }
        
                
        joined_data_mapping = DictUtils.read_dict_from_file(self.json_path)
        join_iterator = JoinIterator(join_statement, joined_data_mapping)




    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/references/join_statement.raw.json")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
