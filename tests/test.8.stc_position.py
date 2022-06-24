"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from mivot_code.client.stc_classes.measure import Position
from mivot_code.utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.8.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        position = Position(xmltree)

        self.assertEqual(position.error.__repr__(), "[Ellipse: [21.157arcsec 13.738arcsec] 61.84deg]")
        self.assertEqual(position.coord.__repr__(), "[LonLatPoint: 253.923544deg -42.8271581deg nanpsec ICRS]")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()