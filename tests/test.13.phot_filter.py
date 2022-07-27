"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from mivot_code.client.class_wrappers.photdm.photcal import PhotCal

from mivot_code.utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.13.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        phot_cal = PhotCal(xmltree)
        
        print(phot_cal)
                
                
                
        print(phot_cal.identifier)
        print(phot_cal.zeroPoint)
        print(phot_cal.photometryFilter)
        print(phot_cal.magnitudeSystem)


         

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()