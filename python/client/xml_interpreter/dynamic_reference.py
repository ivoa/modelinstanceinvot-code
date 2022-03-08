'''
Created on 22 Dec 2021

@author: laurentmichel
'''
from copy import deepcopy
from client.xml_interpreter import logger
from client.xml_interpreter.exceptions import MappingException
from client.xml_interpreter.static_reference_resolver import StaticReferenceResolver

class DynamicReference(object):
    '''
    classdocs
    '''


    def __init__(self, model_view, tag_name, templates_ref, xml_block):
        '''
        Constructor
        '''
        self.resource_seeker = model_view.resource_seeker
        self.annotation_seeker = model_view.annotation_seeker
        self.xml_block = xml_block 
        self.tag_name = tag_name
        self.templates_ref = templates_ref
        self.target_id = None 
        self.fk_col = None
        self.fk_ref = None
        
    def _set_mode(self):
        
        fkey = self.xml_block.xpath("//" + self.tag_name)
        self.target_id = fkey[0].get("dmid")
        if self.target_id is not None:
            logger.info("STATIC ref TODO")
        else:
            logger.info("Dynamic reference")
            self.target_id = fkey[0].get("sourceref")
            fkey = self.xml_block.xpath("//FOREIGN_KEY")
            self.fk_ref = fkey[0].get("ref")
            index_map = self.resource_seeker.get_id_index_mapping(self.templates_ref)
            self.fk_col = index_map[self.fk_ref]
            self.target_xml_block = self.annotation_seeker.get_globals_collection(self.target_id)
            if self.target_xml_block is None:
                raise MappingException("No GLOBALS/COLLECTION with dmid={}".format(self.target_id))
            
    def get_target_instance(self, data_row):
        key = data_row[self.fk_col]
        fkey = self.target_xml_block.xpath("//PRIMARY_KEY[@value='" + key + "']")
        if len(fkey) == 0:
            raise MappingException("GLOBALS/COLLECTION with dmid={} has no item with PRIMARY_KEY={}".format(self.target_id, key))
        elif len(fkey) > 1:
            raise MappingException("GLOBALS/COLLECTION with dmid={} has more than one item with PRIMARY_KEY={}".format(self.target_id, key))
        retour = deepcopy(fkey[0].getparent())
        StaticReferenceResolver.resolve(self.annotation_seeker, None, retour)
        return retour

        


            

    
        