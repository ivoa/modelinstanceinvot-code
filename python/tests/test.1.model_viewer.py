"""
Created on Jan 6, 2022

@author: laurentmichel
"""
import unittest
import os
from astropy.io.votable import parse

from utils.xml_utils import XmlUtils
from utils.dict_utils import DictUtils
from client.xml_interpreter.model_viewer import ModelViewer
class TestModelViewer(unittest.TestCase):

    def test_global_getters(self):      
        self.maxDiff = None
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['_PKTable', 'Results'])
        self.assertDictEqual(self.mviewer.get_globals_models(), 
                             DictUtils.read_dict_from_file(os.path.join(
                                 self.data_path, "data/output/test.1.11.json")))
        self.assertDictEqual(self.mviewer.get_templates_models(), 
                             DictUtils.read_dict_from_file(os.path.join(
                                 self.data_path, "data/output/test.1.12.json")))
          
    def test_(self):
        tlc._connect_table('_PKTable')
        row = tlc.get_next_row()       
        self.assertEqual(row[0], '5813181197970338560')
        self.assertEqual(row[1], 'G')
        
        row = tlc.get_next_row()
        self.assertEqual(row[0], '5813181197970338560')
        self.assertEqual(row[1], 'BP')

        tlc.rewind()
        row = tlc.get_next_row()       
        self.assertEqual(row[0], '5813181197970338560')
        self.assertEqual(row[1], 'G')
                   

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable = parse(os.path.join(self.data_path, "data/input/test.1.xml"))
        
        self.mviewer = None
        for resource in self.votable.resources:
            self.mviewer = ModelViewer(resource, votable_path=os.path.join(self.data_path, "data/input/test.1.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()