'''
Created on 6 avr. 2020

@author: laurentmichel
'''
import re, os
import xmltodict

from schema.validator.validator import Validator
from client.translator.json_mapping_builder import JsonMappingBuilder
from client.translator import logger, schema_dir


class InstanceFromVotable:
    '''
    Translates the mapping block of the input VOTable in dictionary where all mapping elements 
    names are replaced with attribute values
    '''

    def __init__(self, votable_path):
        '''
        Constructor
        :param votable_path: VOTAble path
        :type votable: string
        '''
        self.votable_path = votable_path
        self.vodml_block = None

    def _extract_vodml_block(self):
        '''
        Stores in an intern field the MODEL_INSTANCE block as a string
        Raise an exception in case of failure
        '''
        logger.info("extract vodml block from %s", self.votable_path)
        with open(self.votable_path) as xml_file:
            self.vodml_block = re.search(r'<MODEL_INSTANCE name="[a-zA-Z]*" syntax="ModelInstanceInVot"[^>]*>((.|\n)*?)</MODEL_INSTANCE>', xml_file.read()).group() 
    
        if self.vodml_block is None :
            raise Exception("No vodml block found")
        logger.info("MODEL_INSTANCE found")
        
    def _validate_vodml_block(self):
        '''
        Validates the MODEL_INSTANCE block against the mapping schema
        Raise an exception in case of failure
        '''
        validator = Validator(os.path.join(schema_dir
                                   , "model-instance-in-vot.xsd"))
        if validator.validate_string(self.vodml_block, verbose=True) is True:
            logger.info("MODEL_INSTANCE block is valid")
            self.json_block = xmltodict.parse(self.vodml_block)            
        else:
            logger.error("MODEL_INSTANCE block is not valid")
            raise Exception("MODEL_INSTANCE block is not valid")
        
    def _build_instance(self):
        '''
        Translate the MODEL_INSTANCE block into dict
        '''
        builder = JsonMappingBuilder(json_dict=self.json_block)

        builder.revert_sets("GLOBALS",
                                         default_key='globals')
        # self.builder.revert_compositions("COLLECTION")
        builder.revert_sets("TABLE_MAPPING",
                                         default_key='root')
        builder.revert_array()
        builder.revert_compositions("COLLECTION")
        builder.revert_elements("INSTANCE")
        builder.revert_elements("ATTRIBUTE")
        builder.revert_elements("MODEL")

        self.json_vodml_block = builder.json
        logger.info("JSON MODEL_INSTANCE block built")
        
    """
    def _populate_instance(self, resolve_dmrefs=False):
        '''
        Set the dict with the real values
        :param resolve_refs: Flag for resolving the cross-reference in the mapping. 
                             if true, instance references are replaced with a copy 
                             of the referenced instance
        :type resolve_refs: boolean
        '''
        self._table_mapper = TableMapper(self.votable_path
                                  , json_inst_dict=self.json_vodml_block)
        self._table_mapper.set_element_values(resolve_dmrefs=resolve_refs)
        self._table_mapper.set_array_values()
        self._table_mapper.map_columns()
        logger.info("MODEL_INSTANCE instance created")

    def build_instance(self, resolve_dmrefs=False):
        '''
         This is the public class that must be invoked from outside
         It does the checking and build the model instance that is hosted by 
         an TableMapper instance
        :param resolve_refs: Flag for resolving the cross-reference in the mapping. 
                             if true, instance references are replaced with a copy 
                             of the referenced instance
        :type resolve_refs: boolean
        :return : An TableMapper the contains the dictionary representation of the model 
                  in addition to some getters 
        :rtype: TableMapper instance
        '''
        logger.info("Build in memory instance")

        self._extract_vodml_block()
        self._validate_vodml_block()
        self._build_instance()
        self._populate_instance(resolve_dmrefs=resolve_refs)
        return self._table_mapper
    """
    
        
