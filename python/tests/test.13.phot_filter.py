"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from client.stc_classes.photdm import PhotCal

from utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.13.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        phot_cal = PhotCal(xmltree)
        
        print(phot_cal)

         

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()