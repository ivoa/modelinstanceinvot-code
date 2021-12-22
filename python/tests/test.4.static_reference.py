"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from utils.xml_utils import XmlUtils
from client.xml_interpreter.static_reference_resolver import StaticReferenceResolver
from client.xml_interpreter.mapping_block_cursor import MappingBlockCursor

class TestMapppingBuilder(unittest.TestCase):

    def test_StaticReferenceResolve(self):      
        self.maxDiff = None
        
        mapping_block = XmlUtils.xmltree_from_file(
            os.path.join(self.data_path, "data/input/test.0.xml"))  
        MappingBlockCursor.init(mapping_block.getroot())

        instance = XmlUtils.xmltree_from_file(os.path.join(self.data_path, "data/input/test.4.xml"))
        StaticReferenceResolver.resolve(None, instance)
        XmlUtils.assertXmltreeEqualsFile(instance, 
                                         os.path.join(self.data_path, "data/output/test.4.1.xml"))

        
        
 
 

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()