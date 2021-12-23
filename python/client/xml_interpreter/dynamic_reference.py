'''
Created on 22 Dec 2021

@author: laurentmichel
'''
from copy import deepcopy
from client.xml_interpreter import logger
from client.xml_interpreter.votable_pointer import VOTablePointer
from client.xml_interpreter.mapping_block_cursor import MappingBlockCursor
from client.xml_interpreter.mapping_exception import MappingException
from client.xml_interpreter.static_reference_resolver import StaticReferenceResolver

class DynamicReference(object):
    '''
    classdocs
    '''


    def __init__(self, tag_name, templates_ref, xml_block):
        '''
        Constructor
        '''
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
            logger.info("Dynamic")
            self.target_id = fkey[0].get("tableref")
            fkey = self.xml_block.xpath("//FOREIGN_KEY")
            self.fk_ref = fkey[0].get("ref")
            index_map = VOTablePointer.get_id_index_mapping(self.templates_ref)
            self.fk_col = index_map[self.fk_ref]
            self.target_xml_block = MappingBlockCursor.get_globals_collection(self.target_id)
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
        StaticReferenceResolver.resolve(None, retour)
        return retour

        


            

    
        