"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from client.stc_classes.measure import ProperMotion
from utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.12.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        proper_motion = ProperMotion(xmltree)

        self.assertEqual(proper_motion.error.__repr__(), 
                         "[Bound2D: [[1.0 1.2]mas/year [2.1 2.3]mas/year ]")
        self.assertEqual(proper_motion.coord.__repr__(), 
                         "[LonLatPoint: 1.1mas/year 2.2mas/year None]")
        self.assertEqual(proper_motion.__repr__(), 
                         "ucd: pos.pm coslat:true coords: [LonLatPoint: 1.1mas/year 2.2mas/year None] error: [Bound2D: [[1.0 1.2]mas/year [2.1 2.3]mas/year ]")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()