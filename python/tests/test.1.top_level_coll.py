"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from utils.xml_utils import XmlUtils
from utils.dict_utils import DictUtils
from client.xml_interpreter.mapping_block_cursor import MappingBlockCursor
from client.xml_interpreter.top_level_collection import TopLevelCollection

class TestMapppingBuilder(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        
        tlc = TopLevelCollection(os.path.join(self.data_path, "data/input/test.1.xml"))
        XmlUtils.assertXmltreeEqualsFile(MappingBlockCursor.get_globals(),
                                         os.path.join(self.data_path, "data/output/test.1.1.xml"))
        
        self.assertListEqual(list(MappingBlockCursor.get_tablerefs()), ['_PKTable', 'Results'])
        
        XmlUtils.assertXmltreeEqualsFile(MappingBlockCursor.get_templates_block("Results"),
                                         os.path.join(self.data_path, "data/output/test.1.2.xml"))
        
        tlc.connect_table('_PKTable')
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
        
        tlc._squash_join_and_references()
        
        XmlUtils.assertXmltreeEqualsFile(tlc.top_templates,
                                       os.path.join(self.data_path, "data/output/test.1.3.xml"))
        XmlUtils.assertXmltreeEqualsFile(tlc.references["REFERENCE_2"],
                                       os.path.join(self.data_path, "data/output/test.1.4.xml"))
        XmlUtils.assertXmltreeEqualsFile(tlc.joins["JOIN_6"],
                                       os.path.join(self.data_path, "data/output/test.1.5.xml"))
        model_view = tlc.get_model_view()
        XmlUtils.assertXmltreeEqualsFile(model_view,
                                       os.path.join(self.data_path, "data/output/test.1.8.xml"))

        json_view = tlc.get_json_model_view()
        self.assertListEqual(
            json_view,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.1.9.json"
                )
            ),
        )


    def test_results(self):      
        tlc = TopLevelCollection(os.path.join(self.data_path, "data/input/test.1.xml"))
        
        tlc.connect_table('Results')
        
        tlc._squash_join_and_references()

        tlc._set_column_indices()
        XmlUtils.assertXmltreeEqualsFile(tlc.top_templates,
                                       os.path.join(self.data_path, "data/output/test.1.6.xml"))
        tlc.get_next_row()
        model_view = tlc.get_model_view()    
        XmlUtils.assertXmltreeEqualsFile(model_view,
                                       os.path.join(self.data_path, "data/output/test.1.7.xml"))
        json_view = tlc.get_json_model_view()
        self.assertListEqual(
            json_view,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.1.8.json"
                )
            ),
        )

 

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()