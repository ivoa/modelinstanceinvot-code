'''
Created on 6 avr. 2020

@author: laurentmichel
'''
import re, os
import xmltodict

from client.validator.validator import Validator
from client import logger, schema_path
from client.translator.vocabulary import Ele, Att


class MappingToJson:
    '''
    Translates the mapping block of the input VOTable in dictionary where all mapping elements 
    names are replaced with attribute values
    '''

    def __init__(self, votable_path, exit_validation=True):
        '''
        Constructor
        :param votable_path: VOTAble path
        :type votable: string
        '''
        
        self.exit_validation = exit_validation
        self.votable_path = votable_path
        self.vodml_block = None
        self.json_block = None

    def _extract_vodml_block(self):
        '''
        Stores in an intern field the MODEL_INSTANCE block as a string
        Raise an exception in case of failure
        '''
        logger.info("extract vodml block from %s", self.votable_path)
        with open(self.votable_path) as xml_file:
            content = xml_file.read()
            express = r'<{0}((.|\n)*)>((.|\n)*)</{0}>'.format(Ele.VODML)
            self.vodml_block = re.search(express, content, re.MULTILINE).group() 
    
        if self.vodml_block is None :
            raise Exception("No vodml block found")
        logger.info("VODML found")
        
    def _validate_vodml_block(self):
        '''
        Validates the MODEL_INSTANCE block against the mapping schema
        Raise an exception in case of failure
        '''
        validator = Validator(schema_path)
        if validator.validate_string(self.vodml_block, verbose=True) is True or self.exit_validation is False:
            logger.info("MODEL_INSTANCE block is valid")
            self.json_block = xmltodict.parse(self.vodml_block)    
        else:
            logger.error("MODEL_INSTANCE block is not valid")
            if self.exit_validation is True:
                raise Exception("MODEL_INSTANCE block is not valid")
        
   