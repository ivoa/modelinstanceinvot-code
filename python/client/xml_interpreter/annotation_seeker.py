'''
Created on 11 Dec 2021

@author: laurentmichel
'''
from client.xml_interpreter.exceptions import MappingException
from client.xml_interpreter.vocabulary import Att, Ele
from client import logger


class AnnotationSeeker(object):
    '''
    This class provides tools extracting mapping sub-blocks that often used by others stakeholders
    All functions using the mapping are using this class the get XML elements.
    To make the job simpler for others tools, the XML is namespace removed from the mapping block whatever it is.
    This is usually done by Astropy as well
    '''

    def __init__(self, xml_block):
        '''
        - Split the mapping a elements of interest
        - remove the name_spaces
        - Append numbers to JOIN/REFERENCE
        :param xml_block: XML mapping block (etree.Element)
        '''
        # Full mapping blocks
        self._xml_block = xml_block
        # XML namespace descriptor
        self._nsname = None
        self._nsuri = None
        # GLOBALS bock
        self._globals_block = None
        # Templates dictionary {tableref: XML-TEMPLATES}
        self._templates_blocks = {}
       
        # Get the mapping namespace 
        _namespace  = xml_block.nsmap
        for key, value in _namespace.items():
            self._nsname = key + ':'
            self._nsuri = '{' + value + '}'
            
        # get the GLOBALS block
        for child in self._xml_block:
            if self._name_match(child.tag, Ele.GLOBALS) is True:
                logger.info("Found GLOBALS")
                self._globals_block = child

        # get the TEMPLATES blocks
        for child in self._xml_block:
            if self._name_match(child.tag, Ele.TEMPLATES) is True:
                tableref = child.get("tableref")
                if tableref is not None:
                    logger.info("Found TEMPLATES %s", tableref)
                    self._templates_blocks[tableref] = child
                elif not self._templates_blocks:
                    logger.info("Found TEMPLATES without tableref")
                    self._templates_blocks["DEFAULT"] = child
                else:
                    raise MappingException("TEMPLATES without tableref must be unique")
                
        # remove the namespaces from the element tags that are not changed
        for tag in['INSTANCE', 'ATTRIBUTE', 'COLLECTION', 'GLOBALS', 
                   'TEMPLATES', 'PRIMARY_KEY', 
                   'FOREIGN_KEY', 'WHERE', 'VODML']:
            xpath = './/dm-mapping:' + tag            
            for ele in self._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag 
         
        # remove the namespaces from the element tags that are numbered
        # cannot be identified by role: make them unique to facilitate the job of the resolvers
        cpt = 1
        for tag in['REFERENCE', 'JOIN']:
            xpath = '//dm-mapping:' + tag            
            for ele in self._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag + '_' + str(cpt)
                cpt += 1            
        


    def _name_match(self, name, expected): 
        """
        Returns true if name matches expected whatever the namespace
        """
        return (name.replace(self._nsuri, "") == (expected.replace(self._nsname, "")))
        
    def get_globals(self):
        '''
        GLOBALS getter
        '''
        return self._globals_block 
      
    def get_tablerefs(self):
        '''
        Return the list of all the @tableref found in the mapping
        '''
        return self._templates_blocks.keys()
    
    def get_templates_block(self, tableref):
        '''
        Return the TEMPLATES mapping block of the table matcing @tableref
        :param tableref:
        '''
        return self._templates_blocks[tableref]
    
    def get_globals_collections(self):
        '''
        Returns the list of all GLOBALS/COLLECTION elements.
        These collection have no dmroles but often dmids.
        They have particular roles
        - Used by references (e.g. filter definition)
        - Used as head of the mapped model (e.g. [Cube instance])
        '''
        return self._globals_block.xpath("//GLOBALS/COLLECTION")
    
    def get_globals_collection(self, dmid):
        '''
        Gets the GLOBALS/COLLECTION with @dmid=dmid
        :param dmid:
        '''
        eset =  self._globals_block.xpath("//GLOBALS/COLLECTION[@dmid='" + dmid + "']")
        for ele in eset:
            return ele
        return None

    def get_globals_instances(self):
        '''
        Returns the list of all GLOBALS/INSTANCE elements.
        These collection have no dmroles but often dmids.
        They have particular roles
        - Used by references (e.g. filter definition)
        - Used as head of the mapped model (e.g. Cube instance)
        '''
        return self._globals_block.xpath("//GLOBALS/INSTANCE")
    
    def get_globals_instance_dmtypes(self):
        '''
        Gets the list the @dmtype GLOBALS/INSTANCE
        '''
        retour = []
        for inst in self.get_globals_instances():
            retour.append(inst.get(Att.dmtype))
        return retour
    
    def get_globals_collection_dmtypes(self):
        '''
        Gets the list the @dmtype of GLOBALS/COLLECTION/INSTANCE
        Used for collections of static objects
        '''
        eles = self._globals_block.xpath("//GLOBALS/COLLECTION/INSTANCE")
        retour = []
        for inst in eles:
            dmtype = inst.get(Att.dmtype)
            if dmtype not in retour:
                retour.append(dmtype)
        return retour
   
    def get_globals_instance_dmids(self):
        '''
        Gets the list the @dmid GLOBALS/INSTANCE
        :param dmid:
        '''
        retour = []
        eset =  self._globals_block.xpath("//INSTANCE[@dmid]")
        for ele in eset:
            retour.append(ele.get("dmid"))
        return retour
    
    def get_globals_instance_by_dmid(self, dmid):
        '''
        Gets the GLOBALS/INSTANCE with @dmid=dmid
        :param dmid:
        '''
        eset =  self._globals_block.xpath("//INSTANCE[@dmid='" + dmid + "']")
        for ele in eset:
            return ele
        return None
    
    def get_globals_instance_from_collection(self, sourceref, pk_value):
        '''
        Gets the GLOBALS/COLLECTION[@dmid=sourceref]/INSTANCE/PRIMARY_KEY[@value='pk_value']
        :param dmid:
        '''
        einst =  self._globals_block.xpath("//COLLECTION[@dmid='" + sourceref + "']/INSTANCE/PRIMARY_KEY[@value='" + pk_value + "']")
        for inst in einst:
            return inst.getparent()
        return None
    
    def get_templates_instance_by_dmid(self, tableref, dmid):
        '''
        Gets the TEMPLATES/INSTANCE with @dmid=dmid and TEMPLATES@tableref=tableref
        :param tableref: @tableref of the serarched TEMPLATES
        :param dmid: searched @dmid
        '''
        templates_block = self.get_templates_block(tableref)
        if templates_block is None:
            return None
        eset =  templates_block.xpath(".//INSTANCE[@dmid='" + dmid + "']")
        for ele in eset:
            return ele
        return None
    
    def get_instance_by_dmtype(self, dmtype_pattern):
        '''
        Gets all the mapped instances that have a @dmtype containing dmtype_pattern
        :param dmtype_pattern:
        '''
        retour = {"GLOBALS":[], "TEMPLATES":{}}
        
        eset =  self._globals_block.xpath(".//INSTANCE[contains(@dmtype,'" + dmtype_pattern + "')]")
        retour["GLOBALS"] = eset

        for tableref, block  in self._templates_blocks.items():
            retour["TEMPLATES"][tableref] = block.xpath(".//INSTANCE[contains(@dmtype,'" + dmtype_pattern + "')]")
        return retour
    
    def get_instance_dmtypes(self):
        '''
        Gets @dmtypes of all mapped instances
        '''
        retour = {"GLOBALS":[], "TEMPLATES":{}}
        
        eset =  self._globals_block.xpath(".//INSTANCE")
        for ele in eset:
            retour["GLOBALS"].append(ele.get(Att.dmtype))

        for tableref, block  in self._templates_blocks.items():
            retour["TEMPLATES"][tableref] = []
            eset =  block.xpath(".//INSTANCE")
            for ele in eset:
                retour["TEMPLATES"][tableref].append(ele.get(Att.dmtype))
        return retour
    
    def get_globals_collection_dmids(self):
        '''
        Gets the list of all the @dmid of GLOBALS/COLLECTION
        '''
        retour = []
        eset =  self._globals_block.xpath("//COLLECTION[@dmid]")
        for ele in eset:
            retour.append(ele.get("dmid"))
        return retour
    
    def get_collection_item_by_primarykey(self, coll_dmid, key_value):
        '''
        Get the GLOBALS/COLLECTION/INSTANCE with COLLECTION@dmid=dmid and
        the INSTANCE has a PRIMARY_ke which @value matches key_value
        An exception is risen if there less or more than one element matching the criteria.
        The 2 parameter match the dynamic REFERENCE definition
        :param coll_dmid:
        :param key_value:
        '''
        eset =  self._globals_block.xpath(".//COLLECTION[@dmid='" +coll_dmid + "']/INSTANCE/PRIMARY_KEY[@value='" + key_value + "']")
        if len(eset) == 0:
            raise MappingException("Instance with primary key = {} in collection dmid {} not found".format(key_value, key_value))
        if len(eset) > 1:
            raise MappingException("More than one instance with primary key = {} found in in collection dmid {}".format(key_value, key_value))
        logger.debug("Instance with primary_key=%s found in collection dmid=%s", key_value, coll_dmid)
        return eset[0].getparent()
