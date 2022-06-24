"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from mivot_code.utils.xml_utils import XmlUtils
from mivot_code.client.xml_interpreter.static_reference_resolver import StaticReferenceResolver
from mivot_code.client.xml_interpreter.annotation_seeker import AnnotationSeeker

class TestMapppingBuilder(unittest.TestCase):

    def test_StaticReferenceResolve(self):      
        self.maxDiff = None
        
        mapping_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.0.xml"))  
        aseeker = AnnotationSeeker(mapping_block.getroot())

        instance = XmlUtils.xmltree_from_file(os.path.join(self.data_path, "data/input/test.4.xml"))
        StaticReferenceResolver.resolve(aseeker, None, instance)
        XmlUtils.assertXmltreeEqualsFile(instance, 
                                         os.path.join(self.data_path, "data/output/test.4.1.xml"))

        
        
 
 

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()