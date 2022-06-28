"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from mivot_code.client.class_wrappers.stc_classes.measure import Time
from mivot_code.utils.xml_utils import XmlUtils

class TestSTCGeneric(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.10.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        measure = Time(xmltree)

        self.assertIsNone(measure.error)
        self.assertEqual(measure.coord.__repr__(), "[ISOTime: 2022-01-23 [TT GEOCENTER]]")
        self.assertEqual(measure.__repr__(), "ucd: time coords: [ISOTime: 2022-01-23 [TT GEOCENTER]] error: None")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()