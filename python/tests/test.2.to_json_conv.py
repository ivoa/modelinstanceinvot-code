"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from utils.dict_utils import DictUtils
from astropy.io.votable import parse

from client.xml_interpreter.to_json_converter import ToJsonConverter
from client.xml_interpreter.model_viewer import ModelViewer


class TestToJsonConverter(unittest.TestCase):

 

  
    def test_results(self):  
        '''
        
        '''
        self.maxDiff = None    
        data_path = os.path.dirname(os.path.realpath(__file__))
        votable = parse(os.path.join(data_path, "data/input/test.1.xml"))
        
        mviewer = None
        for resource in votable.resources:
            mviewer = ModelViewer(resource, votable_path=os.path.join(data_path, "data/input/test.1.xml"))
            break;

        mviewer.connect_table('Results')
        mviewer.get_next_row()
        tjc = ToJsonConverter(mviewer.get_model_view())
        
        tjc._translate_xml()
        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(os.path.join(
                    self.data_path, "data/output/test.2.1.json"
                )
            ),
        )

        tjc._revert_collections()
        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.2.json"
                )
            ),
        )


        tjc._revert_attributes()
        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.3.json"
                )
            ),
        )

        tjc._revert_instances()

        self.assertDictEqual(
            tjc.json_instance,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.4.json"
                )
            ),
        )
        
        self.assertListEqual(
            tjc.get_json_instance(),
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.2.5.json"
                )
            ),
        )
 


    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()