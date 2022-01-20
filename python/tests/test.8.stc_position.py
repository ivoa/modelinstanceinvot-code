"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from client.stc_classes.position import Position
from utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.8.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        position = Position(xmltree)

        self.assertEqual(position.error.__repr__(), "[Ellipse: [21.157arcsec 21.157arcsec] 61.84deg]")
        self.assertEqual(position.coord.__repr__(), "[LonLatPoint: 253.923544deg -42.8271581deg psec ICRS]")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()