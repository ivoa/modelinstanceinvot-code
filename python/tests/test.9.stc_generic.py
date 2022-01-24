"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from client.stc_classes.measure import GenericMeasure
from utils.xml_utils import XmlUtils

class TestSTCGeneric(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.9.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        measure = GenericMeasure(xmltree)

        self.assertEqual(measure.error.__repr__(), "[Symmetrical: [0.1]]")
        self.assertEqual(measure.coord.__repr__(), "[PhysicalCoordinate: 0.8 None]")
        self.assertEqual(measure.__repr__(), "ucd: phot.flux;arith.ratio coords: [PhysicalCoordinate: 0.8 None] error: [Symmetrical: [0.1]]")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()