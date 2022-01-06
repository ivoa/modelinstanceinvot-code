"""
Created on Dec 26, 2021

@author: laurentmichel
"""
import unittest
import os
from utils.xml_utils import XmlUtils
from utils.dict_utils import DictUtils
from astropy.io.votable import parse
from client.xml_interpreter.model_viewer import ModelViewer
from client.xml_interpreter.join_operator import JoinOperator

class TestJoinOperator(unittest.TestCase):

    def test_subset(self):      
        self.maxDiff = None
        
        data_path = os.path.dirname(os.path.realpath(__file__))
        votable = parse(os.path.join(data_path, "data/input/test.1.xml"))
        
        mviewer = None
        for resource in votable.resources:
            mviewer = ModelViewer(resource, votable_path=os.path.join(data_path, "data/input/test.1.xml"))
            break;

        mviewer.connect_table('_PKTable')

        mapping_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.0.xml"))  
        
        join_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.6.xml"))  
        join_operator = JoinOperator(mviewer, '_PKTable', join_block)
        join_operator._set_filter()
        join_operator._set_foreign_instance()

        self.assertEqual(str(join_operator.wheres), 
                             "[(foreign: _pksrcid:0  primary: _pksrcid:0), (foreign: _pkband:2  primary: _pkband:1)]")
        self.assertEqual(join_operator.target_table_id, 'Results')
        
        row = mviewer.get_next_row()       
        for line in join_operator.get_matching_data(row):
            self.assertEqual(line[0], "5813181197970338560")
            self.assertEqual(line[2], "G")
        
        XmlUtils.assertXmltreeEqualsFile(join_operator.get_matching_model_view()[0], 
                os.path.join(
                    self.data_path, "data/output/test.6.3.xml"
                ))
             
        self.assertDictEqual(
            join_operator.get_json_json_model_view()[0],
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.6.1.json"
                )
            )
        )
        self.assertDictEqual(
            join_operator.get_json_json_model_view()[1],
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.6.2.json"
                )
            )
        )

  
    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()