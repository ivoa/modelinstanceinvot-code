'''
Created on 11 Dec 2021

@author: laurentmichel
'''
from client.objectbuilder.mapping_exception import MappingException
from client.translator.vocabulary import Att, Ele
class MappingBlockPointer(object):
    '''
    classdocs
    '''

    _json_block = None
    _globals_block = None
    _templates_block = None

    @staticmethod    
    def init(json_block):
        '''
        Constructor
        '''
        MappingBlockPointer._json_block = json_block[Ele.VODML]
        
      
        
    @staticmethod    
    def get_globals():
        if MappingBlockPointer._json_block is None:
            raise MappingException("MappingBlockPointer not initialized")
        if MappingBlockPointer._globals_block is not None:
            return MappingBlockPointer._globals_block
        for key, obj in MappingBlockPointer._json_block.items():
            if key == Ele.GLOBALS:
                MappingBlockPointer._globals_block = obj
                return obj
        raise MappingException("No GLOBALS element in mapping blocks")
    
    @staticmethod    
    def get_templates_blocks():
        if MappingBlockPointer._json_block is None:
            raise MappingException("MappingBlockPointer not initialized")
        if MappingBlockPointer._templates_block is not None:
            return MappingBlockPointer._templates_block
        for key, obj in MappingBlockPointer._json_block.items():
            if key == Ele.TEMPLATES:
                MappingBlockPointer._templates_block = obj
                return obj
        raise MappingException("No TEMPLATES element in mapping blocks")
                 
    
    @staticmethod    
    def get_globals_collection(dmid):
        if MappingBlockPointer._json_block is None:
            raise MappingException("MappingBlockPointer not initialized")
        pass

    @staticmethod    
    def get_globals_object(dmtype):
        if MappingBlockPointer._json_block is None:
            raise MappingException("MappingBlockPointer not initialized")
        globals_block = MappingBlockPointer.get_globals()()
        for obj in globals_block:
            if obj[Att.dmtype] == dmtype:
                return obj

        raise MappingException("GLOBALS object with @dmtype={} not found".format(dmtype))
   
    @staticmethod    
    def get_templates(tableref):
        if MappingBlockPointer._json_block is None:
            raise MappingException("MappingBlockPointer not initialized")
        templates_block = MappingBlockPointer.get_templates_blocks()
        for obj in templates_block:
            if obj[Att.tableref] == tableref:
                return obj

        raise MappingException("TEMPLATES with @tableref={} not found".format(tableref))
    
    
    
    