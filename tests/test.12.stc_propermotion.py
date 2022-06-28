"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from mivot_code.client.class_wrappers.stc_classes.measure import ProperMotion
from mivot_code.utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.12.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        proper_motion = ProperMotion(xmltree)

        self.assertEqual(proper_motion.error.__repr__(), 
                         "[[1.0 1.2]mas/year [2.1 2.3]mas/year‘]]")
        self.assertEqual(proper_motion.coord.__repr__(), 
                         "[1.1 mas/year 2.2 mas/year]")
        self.assertEqual(proper_motion.__repr__(), 
                         "pos.pm=[1.1 mas/year 2.2 mas/year] +/-[[1.0 1.2]mas/year [2.1 2.3]mas/year‘]]")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()