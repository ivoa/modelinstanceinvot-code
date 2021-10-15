'''
Created on 30 août 2021

@author: michel
'''
import re
import xml.etree.cElementTree as ET
from astropy.io.votable import parse
from client import logger, schema_path
from client.validator.validator import Validator

class ResourceSelector(object):
    '''
    classdocs
    '''

    def __init__(self, votable_path):
        '''
        Constructor
        '''
        self.votable_path = votable_path
        self._is_valid = False
        self._is_mapped = False
        self.tables = None
    
    @property
    def is_valid(self):
        return self._is_valid
    
    @property
    def is_mapped(self):
        return self._is_mapped
    
    def validate(self):
        logger.info("checking %s", self.votable_path)

        tree = ET.parse(self.votable_path)
        rootxml = tree.getroot()
        namespace=""
        sns = re.search('{.*}', rootxml.tag)
        if sns:
            namespace =  sns.group(0)

        top_resources = tree.findall("{}RESOURCE[@type='results']".format(namespace))
        if len(top_resources) != 1 :
            logger.error("Only one top level resource of type results is supported")
            self._is_valid = False
            return False
        
        top_resource = top_resources[0]
        meta_resources = top_resource.findall("{}RESOURCE[@type='meta']".format(namespace))
        if len(meta_resources) > 1 :
            logger.error("Only one top child resource of type meta is supported")
            self._is_valid = False
            self._is_mapped = True
            return False
        elif len(meta_resources) == 0 :
            logger.info("no mapping block detected")
            self._is_valid = True
            self._is_mapped = False
            return False

        meta_resources = top_resource.find("{}RESOURCE".format(namespace))
        if len(meta_resources) > 1 :
            logger.error("Top level results resource cannot contain more than one resource")
            self._is_valid = False
            self._is_mapped = False
            return False

        meta_resource = top_resource.find("{}RESOURCE[1]".format(namespace))
        if self._is_mapped is True and meta_resource.attrib["type"] != "meta" :
            logger.error("The mapping block must be at the top level within the results resource")
            self._is_valid = False
            self._is_mapped = False
            return False
        else: 
            vodml_block = ET.tostring(meta_resource.find("*[1]"), encoding="unicode").replace("ns0", "dm-mapping")
            validator = Validator(schema_path)
            if validator.validate_string(vodml_block, verbose=True) is True or self.exit_validation is False:
                logger.info("Mapping block block is valid")
                self._is_valid = True
                self._is_mapped = True
                return True

            else:
                logger.error("mapping block is not valid")
                self._is_valid = False
                self._is_mapped = False
                return False

    def map_table(self):
        if self.is_valid is False:
            logger.error("cannot map tables of a non valid votable")
            return
        votable = parse(self.votable_path) 
        for resource in votable.resources:
            self.tables = {}
            for table in resource.tables:
                key = table.ID
                if not key:
                    key = table.name
                logger.info("add table %s", key)
                self.tables[key] = table

