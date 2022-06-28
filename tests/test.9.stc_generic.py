"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from mivot_code.client.class_wrappers.stc_classes.measure import GenericMeasure
from mivot_code.utils.xml_utils import XmlUtils

class TestSTCGeneric(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.9.xml")
        
        xmltree = XmlUtils.xmltree_from_file(vpath)
        measure = GenericMeasure(xmltree)

        self.assertEqual(measure.error.__repr__(), "0.1 ")
        self.assertEqual(measure.coord.__repr__(), "[0.8 ]")
        self.assertEqual(measure.__repr__(), "phot.flux;arith.ratio=[0.8 ] +/-0.1 ")
        

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()