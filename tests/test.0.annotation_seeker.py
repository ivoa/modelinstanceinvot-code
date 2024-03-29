"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from mivot_code.utils.xml_utils import XmlUtils
from mivot_code.client.xml_interpreter.annotation_seeker import AnnotationSeeker
from mivot_code.utils.dict_utils import DictUtils

class TestMapppingBuilder(unittest.TestCase):

    def test_all_reverts(self):      
        
        mapping_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.0.xml"))  
        
        aseeker = AnnotationSeeker(mapping_block.getroot())

        XmlUtils.assertXmltreeEqualsFile(aseeker.get_globals(),
                                         os.path.join(self.data_path, "data/output/test.0.1.xml"))
        
        self.assertListEqual(list(aseeker.get_tablerefs()), ['_PKTable', 'Results'])
        
        XmlUtils.assertXmltreeEqualsFile(aseeker.get_templates_block("Results"),
                                         os.path.join(self.data_path, "data/output/test.0.2.xml"))

        self.assertEqual(len(aseeker.get_globals_collections()), 2)
        
        self.assertEqual(len(aseeker.get_globals_instances()), 1)
        
        self.assertListEqual(aseeker.get_globals_instance_dmtypes(), ['ds:experiment.Target'])
        
        self.assertListEqual(aseeker.get_globals_instance_dmids(),
              ['_timesys', '_spacesys1', '_photsys_G', '_photsys_RP', '_photsys_BP',
                '_ds1', '_tg1', '_TimeSeries', '_ts_data'])
        
        self.assertListEqual(aseeker.get_globals_collection_dmids(),
                             ['_CoordinateSystems', '_Datasets'])
        
        XmlUtils.assertXmltreeEqualsFile(aseeker.get_globals_instance_by_dmid('_ts_data'),
                                         os.path.join(self.data_path, "data/output/test.0.3.xml"))
        
        selection = aseeker.get_instance_by_dmtype("coords")
        self.assertEqual(len(selection["GLOBALS"]), 5)
        for ele in selection["GLOBALS"]:
            self.assertTrue(ele.get("dmtype").startswith("coords")
                            , "dmtype " + ele.get("dmtype") + " does not match the coords pattern")
            
        self.assertEqual(len(selection["TEMPLATES"]["_PKTable"]), 0)
        self.assertEqual(len(selection["TEMPLATES"]["Results"]), 3)
        for _ , table_sel in selection["TEMPLATES"].items():
            for ele in table_sel:
                self.assertTrue(ele.get("dmtype").startswith("coords")
                            , "dmtype " + ele.get("dmtype") + " does not match the coords pattern")
        
        pksel = aseeker.get_collection_item_by_primarykey("_Datasets", "5813181197970338560")
        XmlUtils.assertXmltreeEqualsFile(pksel,
                                         os.path.join(self.data_path, "data/output/test.0.4.xml"))
        
        self.assertDictEqual(aseeker.get_instance_dmtypes(),
                             DictUtils.read_dict_from_file(os.path.join(self.data_path, "data/output/test.0.5.json")))

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()