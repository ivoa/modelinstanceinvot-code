"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from utils.xml_utils import XmlUtils
from client.xml_interpreter.mapping_block_cursor import MappingBlockCursor

class TestMapppingBuilder(unittest.TestCase):

    def test_all_reverts(self):      
        
        mapping_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.0.xml"))  
        MappingBlockCursor.init(mapping_block.getroot())

        XmlUtils.assertXmltreeEqualsFile(MappingBlockCursor.get_globals(),
                                         os.path.join(self.data_path, "data/output/test.0.1.xml"))
        
        self.assertListEqual(list(MappingBlockCursor.get_tablerefs()), ['_PKTable', 'Results'])
        
        XmlUtils.assertXmltreeEqualsFile(MappingBlockCursor.get_templates_block("Results"),
                                         os.path.join(self.data_path, "data/output/test.0.2.xml"))

        self.assertEqual(len(MappingBlockCursor.get_globals_collections()), 2)
        
        self.assertEqual(len(MappingBlockCursor.get_globals_instances()), 1)
        
        self.assertListEqual(MappingBlockCursor.get_globals_instance_dmtypes(), ['ds:experiment.Target'])
        
        self.assertListEqual(MappingBlockCursor.get_globals_instance_dmids(),
              ['_timesys', '_spacesys1', '_photsys_G', '_photsys_RP', '_photsys_BP',
                '_ds1', '_tg1', '_TimeSeries', '_ts_data'])
        
        self.assertListEqual(MappingBlockCursor.get_globals_collection_dmids(),
                             ['_CoordinateSystems', '_Datasets'])
        
        XmlUtils.assertXmltreeEqualsFile(MappingBlockCursor.get_globals_instance_by_dmid('_ts_data'),
                                         os.path.join(self.data_path, "data/output/test.0.3.xml"))
        
        selection = MappingBlockCursor.get_instance_by_dmtype("coords")
        self.assertEqual(len(selection["GLOBALS"]), 5)
        for ele in selection["GLOBALS"]:
            self.assertTrue(ele.get("dmtype").startswith("coords")
                            , "dmtype " + ele.get("dmtype") + " does not match the coords pattern")
            
        self.assertEqual(len(selection["TEMPLATES"]["_PKTable"]), 0)
        self.assertEqual(len(selection["TEMPLATES"]["Results"]), 3)
        for tableref, table_sel in selection["TEMPLATES"].items():
            for ele in table_sel:
                self.assertTrue(ele.get("dmtype").startswith("coords")
                            , "dmtype " + ele.get("dmtype") + " does not match the coords pattern")
        
        pksel = MappingBlockCursor.get_collection_item_by_primarykey("_Datasets", "5813181197970338560")
        XmlUtils.assertXmltreeEqualsFile(pksel,
                                         os.path.join(self.data_path, "data/output/test.0.4.xml"))

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()