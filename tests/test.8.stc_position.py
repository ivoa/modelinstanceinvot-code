"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from mivot_code.client.class_wrappers.stc_classes.measure import Position
from mivot_code.utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.8.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        position = Position(xmltree)

        self.assertEqual(position.error.__repr__(), "21.157 arcsec 13.738 arcsec 61.84 deg")
        self.assertEqual(position.coord.__repr__(), "[253.923544 deg -42.8271581 deg nan psec]")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()