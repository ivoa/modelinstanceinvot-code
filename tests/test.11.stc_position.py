"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from mivot_code.client.class_wrappers.stc_classes.measure import Velocity
from mivot_code.utils.xml_utils import XmlUtils

class TestSTCPosition(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.11.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        velocity = Velocity(xmltree)

        self.assertEqual(velocity.error.__repr__(), 
                         "[[1.0 1.2]mas/year [2.1 2.3]mas/year [2345.0 2399.0]km/sec]")
        self.assertEqual(velocity.coord.__repr__(), 
                         "[1.1 mas/year 2.2 mas/year 2345.98 km/sec]")
        self.assertEqual(velocity.__repr__(), 
                         "phys.veloc=[1.1 mas/year 2.2 mas/year 2345.98 km/sec] +/-[[1.0 1.2]mas/year [2.1 2.3]mas/year [2345.0 2399.0]km/sec]")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()