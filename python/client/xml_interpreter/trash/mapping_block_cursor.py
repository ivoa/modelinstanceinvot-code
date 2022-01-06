'''
Created on 11 Dec 2021

@author: laurentmichel
'''
from client.xml_interpreter.mapping_exception import MappingException
from client.xml_interpreter.vocabulary import Att, Ele
from client.translator import logger


class MappingBlockCursor(object):
    '''
    This class provides tools extracting mapping sub-blocks that often used by others stakeholders
    All functions using the mapping are using this class the get XML elements.
    To make the job simpler for others tools, the XML is namespace removed from the mapping block whatever it is.
    TODO At the time of writing the class is static in order to be callable from any part of the code.
    This feature should be made thread-safe in a public release
    '''
    # Full mapping blocks
    _xml_block = None
    # XML namespace descriptor
    _nsname = None
    _nsuri = None
    # GLOBALS bock
    _globals_block = None
    # Templates dictionary {tableref: XML-TEMPLATES}
    _templates_blocks = {}

    @staticmethod    
    def init(xml_block):
        '''
        - Split the mapping a elements of interest
        - remove the name_spaces
        - Append numbers to JOIN/REFERENCE
        :param xml_block: XML mapping block (etree.Element)
        '''
        
        MappingBlockCursor._xml_block = xml_block
        # Get the mapping namespace 
        _namespace  = xml_block.nsmap
        for key, value in _namespace.items():
            MappingBlockCursor._nsname = key + ':'
            MappingBlockCursor._nsuri = '{' + value + '}'
            
        # get the GLOBALS block
        for child in MappingBlockCursor._xml_block:
            if MappingBlockCursor._name_match(child.tag, Ele.GLOBALS) is True:
                logger.info("Found GLOBALS")
                MappingBlockCursor._globals_block = child

        # get the TEMPLATES blocks
        for child in MappingBlockCursor._xml_block:
            if MappingBlockCursor._name_match(child.tag, Ele.TEMPLATES) is True:
                tableref = child.get("tableref")
                if tableref is not None:
                    logger.info("Found TEMPLATES %s", tableref)
                    MappingBlockCursor._templates_blocks[tableref] = child
                elif not MappingBlockCursor._templates_blocks:
                    logger.info("Found TEMPLATES without tableref")
                    MappingBlockCursor._templates_blocks["DEFAULT"] = child
                else:
                    raise MappingException("TEMPLATES without tableref must be unique")
                
        # remove the namespaces from the element tags that are not changed
        for tag in['INSTANCE', 'ATTRIBUTE', 'COLLECTION', 'GLOBALS', 
                   'TEMPLATES', 'PRIMARY_KEY', 
                   'FOREIGN_KEY', 'WHERE', 'VODML']:
            xpath = './/dm-mapping:' + tag            
            for ele in MappingBlockCursor._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag 
         
        # remove the namespaces from the element tags that are numbered
        # cannot be identified by role: make them unique to facilitate the job of the resolvers
        cpt = 1
        for tag in['REFERENCE', 'JOIN']:
            xpath = '//dm-mapping:' + tag            
            for ele in MappingBlockCursor._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag + '_' + str(cpt)
                cpt += 1            
        

    @staticmethod    
    def _name_match(name, expected): 
        """
        Returns true if name matches expected whatever the namespace
        """
        return (name.replace(MappingBlockCursor._nsuri, "") == (expected.replace(MappingBlockCursor._nsname, "")))
        
    @staticmethod    
    def get_globals():
        '''
        GLOBALS getter
        '''
        return MappingBlockCursor._globals_block 
      
    @staticmethod    
    def get_tablerefs():
        '''
        Return the list of all the @tableref found in the mapping
        '''
        return MappingBlockCursor._templates_blocks.keys()
    
    @staticmethod    
    def get_templates_block(tableref):
        '''
        Return the TEMPLATES mapping block of the table matcing @tableref
        :param tableref:
        '''
        return MappingBlockCursor._templates_blocks[tableref]
    
    @staticmethod    
    def get_globals_collections():
        '''
        Returns the list of all GLOBALS/COLLECTION elements.
        These collection have no dmroles but often dmids.
        They have particular roles
        - Used by references (e.g. filter definition)
        - Used as head of the mapped model (e.g. [Cube instance])
        '''
        return MappingBlockCursor._globals_block.xpath("//GLOBALS/COLLECTION")
    
    @staticmethod    
    def get_globals_collection(dmid):
        '''
        Gets the GLOBALS/COLLECTION with @dmid=dmid
        :param dmid:
        '''
        eset =  MappingBlockCursor._globals_block.xpath("//GLOBALS/COLLECTION[@dmid='" + dmid + "']")
        for ele in eset:
            return ele
        return None

    @staticmethod    
    def get_globals_instances():
        '''
        Returns the list of all GLOBALS/INSTANCE elements.
        These collection have no dmroles but often dmids.
        They have particular roles
        - Used by references (e.g. filter definition)
        - Used as head of the mapped model (e.g. Cube instance)
        '''
        return MappingBlockCursor._globals_block.xpath("//GLOBALS/INSTANCE")
    
    @staticmethod    
    def get_globals_instance_dmtypes():
        '''
        Gets the list the @dmtype GLOBALS/INSTANCE
        :param dmtype:
        '''
        retour = []
        for inst in MappingBlockCursor.get_globals_instances():
            retour.append(inst.get(Att.dmtype))
        return retour
   
    @staticmethod    
    def get_globals_instance_dmids():
        '''
        Gets the list the @dmid GLOBALS/INSTANCE
        :param dmid:
        '''
        retour = []
        eset =  MappingBlockCursor._globals_block.xpath("//INSTANCE[@dmid]")
        for ele in eset:
            retour.append(ele.get("dmid"))
        return retour
    
    @staticmethod    
    def get_globals_instance_by_dmid(dmid):
        '''
        Gets the GLOBALS/INSTANCE with @dmid=dmid
        :param dmid:
        '''
        eset =  MappingBlockCursor._globals_block.xpath("//INSTANCE[@dmid='" + dmid + "']")
        for ele in eset:
            return ele
        return None
    
    @staticmethod    
    def get_templates_instance_by_dmid(tableref, dmid):
        '''
        Gets the TEMPLATES/INSTANCE with @dmid=dmid and TEMPLATES@tableref=tableref
        :param tableref: @tableref of the serarched TEMPLATES
        :param dmid: searched @dmid
        '''
        templates_block = MappingBlockCursor.get_templates_block(tableref)
        if templates_block is None:
            return None
        eset =  templates_block.xpath(".//INSTANCE[@dmid='" + dmid + "']")
        for ele in eset:
            return ele
        return None
    
    @staticmethod    
    def get_instance_by_dmtype(dmtype_pattern):
        '''
        Gets all the mapped instances that have a @dmrtype containing dmtype_pattern
        :param dmtype_pattern:
        '''
        retour = {"GLOBALS":[], "TEMPLATES":{}}
        
        eset =  MappingBlockCursor._globals_block.xpath(".//INSTANCE[contains(@dmtype,'" + dmtype_pattern + "')]")
        retour["GLOBALS"] = eset

        for tableref, block  in MappingBlockCursor._templates_blocks.items():
            retour["TEMPLATES"][tableref] = block.xpath(".//INSTANCE[contains(@dmtype,'" + dmtype_pattern + "')]")
        return retour
    
    @staticmethod    
    def get_globals_collection_dmids():
        '''
        Gets the list of all the @dmid of GLOBALS/COLLECTION
        '''
        retour = []
        eset =  MappingBlockCursor._globals_block.xpath("//COLLECTION[@dmid]")
        for ele in eset:
            retour.append(ele.get("dmid"))
        return retour
    
    @staticmethod    
    def get_collection_item_by_primarykey(coll_dmid, key_value):
        '''
        Get the GLOBALS/COLLECTION/INSTANCE with COLLECTION@dmid=dmid and
        the INSTANCE has a PRIMARY_ke which @value matches key_value
        An exception is risen if there less or more than one element matching the criteria.
        The 2 parameter match the dynamic REFERENCE definition
        :param coll_dmid:
        :param key_value:
        '''
        eset =  MappingBlockCursor._globals_block.xpath(".//COLLECTION[@dmid='" +coll_dmid + "']/INSTANCE/PRIMARY_KEY[@value='" + key_value + "']")
        if len(eset) == 0:
            raise MappingException("Instance with primary key = {} in collection dmid {} not found".format(key_value, key_value))
        if len(eset) > 1:
            raise MappingException("More than one instance with primary key = {} found in in collection dmid {}".format(key_value, key_value))
        logger.debug("Instance with primary_key=%s found in collection dmid=%s", key_value, coll_dmid)
        return eset[0].getparent()
