'''
Created on 16 Dec 2021

@author: laurentmichel
'''
import xmltodict
from lxml import etree
from unittest import TestCase

class XmlUtils(object):
    '''
    classdocs
    '''

    @staticmethod
    def pretty_print(xmltree):
        print(XmlUtils.pretty_string(xmltree))
        
    @staticmethod
    def pretty_string(xmltree):
        return etree.tostring(xmltree, pretty_print=True).decode("utf-8")

    @staticmethod
    def xmltree_from_file(file_path):
        return etree.parse(file_path)
    
    @staticmethod
    def xmltree_to_file(xmltree, file_path):
        with open(file_path, 'w') as output:
            output.write(XmlUtils.pretty_string(xmltree))
            
    @staticmethod
    def assertXmltreeEquals(xmltree1, xmltree2, message):
        dict1 = xmltodict.parse(etree.tostring(xmltree1))
        dict2 = xmltodict.parse(etree.tostring(xmltree2))
        TestCase().assertDictEqual(dict1, dict2, message)
        
    @staticmethod
    def assertXmltreeEqualsFile(xmltree1, xmltree2_file, message=""):
        dict1 = xmltodict.parse(etree.tostring(xmltree1))
        dict2 = xmltodict.parse(etree.tostring(XmlUtils.xmltree_from_file(xmltree2_file)))
        TestCase().assertDictEqual(dict1, dict2, message)
    
    
    

        