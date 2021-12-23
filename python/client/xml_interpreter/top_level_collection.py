'''
Created on 16 Dec 2021

@author: laurentmichel
'''
import re
import lxml
import xmltodict
from copy import deepcopy
from numpy import  float64

from client.xml_interpreter import logger
from utils.xml_utils import XmlUtils
from client.xml_interpreter.votable_pointer import VOTablePointer
from client.xml_interpreter.mapping_exception import MappingException
from client.xml_interpreter.mapping_block_cursor import MappingBlockCursor
from client.xml_interpreter.table_iterator import TableIterator
from client.xml_interpreter.json_block_extractor import JsonBlockExtractor
from client.xml_interpreter.to_json_converter import ToJsonConverter
from client.xml_interpreter.dynamic_reference import DynamicReference
from client.xml_interpreter.static_reference_resolver import StaticReferenceResolver
class TopLevelCollection(object):
    '''
    classdocs
    '''

    def __init__(self, votable_path):
        '''
        Constructor
        ''' 
        self.votable_path = votable_path
        self.mapping_block = None
        self.top_table = None
        self.table_ref = None
        self.table_iterator = None
        self.top_templates = None
        self.last_row = None
        self.references = {}
        self.joins = {}
        VOTablePointer.connect(votable_path)
        self._extract_mapping_block()
        MappingBlockCursor.init(self.mapping_block)

       
    def _extract_mapping_block(self):
        logger.info("extract vodml block from %s", self.votable_path)
        with open(self.votable_path) as xml_file:
            content = xml_file.read()
            start = content.index('<dm-mapping:VODML')
            if start == -1:
                raise MappingException("Cannot find mapping block")
            content = content[start:]
            stop_pattern = '</dm-mapping:VODML>'
            stop = content.index(stop_pattern) + len(stop_pattern)
            content = content[:stop]
            self.mapping_block = lxml.etree.fromstring(content)

        logger.info("VODML found")

    def connect_table(self, tableref):
        self.table_ref = tableref
        self.top_table = VOTablePointer.get_table(tableref)
        if self.top_table is None:
            raise MappingException("Cannot find table {} in VOTable".format(tableref))
        logger.debug("table %s found in VOTable", tableref)
        
        self.top_templates = deepcopy(MappingBlockCursor.get_templates_block(tableref))
        if self.top_templates is None:
            raise MappingException("Cannot find TEMPLATES {} ".format(tableref))
        logger.debug("TEMPLATES %s found ", tableref)
        
        self.table_iterator = TableIterator(tableref, self.top_table.to_table())
        
    def _squash_join_and_references(self):
        for ele in self.top_templates.xpath("//*[starts-with(name(), 'REFERENCE_')]"):
            self.references = {ele.tag: deepcopy(ele)}
            for child in list(ele):
                ele.remove(child)
        
        for ele in self.top_templates.xpath("//*[starts-with(name(), 'JOIN')]"):
            self.joins = {ele.tag: deepcopy(ele)}
            for child in list(ele):
                ele.remove(child)    
                    
    def _set_column_indices(self):
        index_map = VOTablePointer.get_id_index_mapping(self.table_ref)
        for ele in self.top_templates.xpath("//ATTRIBUTE"):
            ref = ele.get("ref")
            if ref is not None:
                ele.attrib["index"] = str(index_map[ref])
         
    def rewind(self):
        self.table_iterator._rewind()
    
    def get_next_row(self):
        self.last_row = self.table_iterator._get_next_row()
        return self.last_row
    
    def get_last_row(self):    
        return self.last_row

    def get_model_view(self):
        templates_copy = deepcopy(self.top_templates)
        StaticReferenceResolver.resolve(self.table_ref, templates_copy)
        for ele in templates_copy.xpath("//ATTRIBUTE"):
            ref = ele.get("ref")
            if ref is not None:
                index = ele.attrib["index"]
                ele.attrib["value"] = str(self.last_row[int(index)])
        for dref_tag, dref in self.references.items():
            logger.info("resolve reference %s", dref_tag)
            dyn_resolver = DynamicReference(dref_tag, self.table_ref, dref)
            dyn_resolver._set_mode()
            ref_target = dyn_resolver.get_target_instance(self.get_last_row())
            ref_element = templates_copy.xpath("//" + dref_tag)[0]
            ref_host = ref_element.getparent()
            ref_target_copy = deepcopy(ref_target)
            # Set the reference role to the copied instance
            ref_target_copy.attrib["dmrole"] = ref_element.get('dmrole')
            # Insert the referenced object
            ref_host.append(ref_target_copy)
            # Drop the reference
            ref_host.remove(ref_element)

            
        return templates_copy
    
    def get_json_model_view(self):
        logger.debug("build json view")
        tjc = ToJsonConverter(self.get_model_view())
        return tjc.get_json_instance()
        
    def get_json_model_component_by_type(self, searched_type):
        json_view = self.get_json_model_view()
        return JsonBlockExtractor.search_subelement_by_type(json_view, searched_type)
    
    def get_mapped_models(self):
        pass
