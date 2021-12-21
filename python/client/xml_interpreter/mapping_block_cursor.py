'''
Created on 11 Dec 2021

@author: laurentmichel
'''
from client.xml_interpreter.mapping_exception import MappingException
from client.xml_interpreter.vocabulary import Att, Ele
from client.translator import logger
import xmltodict, lxml
from utils.dict_utils import DictUtils
from client.translator.json_mapping_builder import JsonMappingBuilder
from client.objectbuilder.json_block_extractor import JsonBlockExtractor
from utils.xml_utils import XmlUtils

class MappingBlockCursor(object):
    '''
    classdocs
    '''

    _xml_block = None
    _nsname = None
    _nsuri = None
    _globals_block = None
    _templates_blocks = {}

    @staticmethod    
    def init(xml_block):
        '''
        Constructor
        '''
        MappingBlockCursor._xml_block = xml_block
        _namespace  = xml_block.nsmap
        for key, value in _namespace.items():
            MappingBlockCursor._nsname = key + ':'
            MappingBlockCursor._nsuri = '{' + value + '}'
            

        for child in MappingBlockCursor._xml_block:
            if MappingBlockCursor._name_match(child.tag, Ele.GLOBALS) is True:
                logger.info("Found GLOBALS")
                MappingBlockCursor._globals_block = child

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
                
        for tag in['INSTANCE', 'ATTRIBUTE', 'COLLECTION', 'GLOBALS', 
                   'TEMPLATES', 'PRIMARY_KEY', 
                   'FOREIGN_KEY', 'WHERE', 'VODML']:
            xpath = './/dm-mapping:' + tag            
            for ele in MappingBlockCursor._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag 
                
        # cannot be identified by role: make them uniques
        cpt = 1
        for tag in['REFERENCE', 'JOIN']:
            xpath = '//dm-mapping:' + tag            
            for ele in MappingBlockCursor._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag + '_' + str(cpt)
                cpt += 1
            
        

    @staticmethod    
    def _name_match(name, expected): 
        """
        Returns true if name matches expected whetever the namespace
        """
        return (name.replace(MappingBlockCursor._nsuri, "") == (expected.replace(MappingBlockCursor._nsname, "")))
        
    @staticmethod    
    def get_globals():
        return MappingBlockCursor._globals_block 
      
    @staticmethod    
    def get_tablerefs():
        return MappingBlockCursor._templates_blocks.keys()
    
    @staticmethod    
    def get_templates_block(tableref):
        return MappingBlockCursor._templates_blocks[tableref]
    
    @staticmethod    
    def get_globals_collections():
        return MappingBlockCursor._globals_block.xpath("//GLOBALS/COLLECTION")
    
    @staticmethod    
    def get_globals_collection(dmid):
        return MappingBlockCursor._globals_block.xpath("//GLOBALS/COLLECTION")

    @staticmethod    
    def get_globals_instances():
        return MappingBlockCursor._globals_block.xpath("//GLOBALS/INSTANCE")
    
    @staticmethod    
    def get_globals_instance_dmtypes():
        retour = []
        for inst in MappingBlockCursor.get_globals_instances():
            retour.append(inst.get(Att.dmtype))
        return retour
   
    @staticmethod    
    def get_globals_instance_dmids():
        retour = []
        eset =  MappingBlockCursor._globals_block.xpath("//INSTANCE[@dmid]")
        for ele in eset:
            retour.append(ele.get("dmid"))
        return retour
    
    @staticmethod    
    def get_globals_instance_by_dmid(dmid):
        eset =  MappingBlockCursor._globals_block.xpath("//INSTANCE[@dmid='" + dmid + "']")
        for ele in eset:
            return ele
        return None
    
    @staticmethod    
    def get_instance_by_dmtype(dmtype_pattern):
        retour = {"GLOBALS":[], "TEMPLATES":{}}
        
        eset =  MappingBlockCursor._globals_block.xpath(".//INSTANCE[contains(@dmtype,'" + dmtype_pattern + "')]")
        retour["GLOBALS"] = eset

        for tableref, block  in MappingBlockCursor._templates_blocks.items():
            retour["TEMPLATES"][tableref] = block.xpath(".//INSTANCE[contains(@dmtype,'" + dmtype_pattern + "')]")
        return retour
    
    @staticmethod    
    def get_globals_collection_dmids():
        retour = []
        eset =  MappingBlockCursor._globals_block.xpath("//COLLECTION[@dmid]")
        for ele in eset:
            retour.append(ele.get("dmid"))
        return retour
    
    @staticmethod    
    def get_collection_item_by_primarykey(coll_dmid, key_value):
        eset =  MappingBlockCursor._globals_block.xpath(".//COLLECTION[@dmid='" +coll_dmid + "']/INSTANCE/PRIMARY_KEY[@value='" + key_value + "']")
        if len(eset) == 0:
            raise MappingException("Instance with primary key = {} in collection dmid {} not found".format(key_value, key_value))
        if len(eset) > 1:
            raise MappingException("More than one instance with primary key = {} found in in collection dmid {}".format(key_value, key_value))
        logger.debug("Instance with primary_key=%s found in collection dmid=%s", key_value, coll_dmid)
        return eset[0].getparent()


   
    @staticmethod    
    def get_json_block():
        retour  = {"GLOBALS":[], 'TEMPLATES': {}}
        json_block =  xmltodict.parse(lxml.etree.tostring(MappingBlockCursor._xml_block))
        #DictUtils.print_pretty_json(json_block)
        globals_block = json_block['VODML']['GLOBALS']

        DictUtils.print_pretty_json(globals_block)

        for key, value in globals_block.items():
            value.pop("@dmrole")
            if key.startswith('COLLECTION'):
                retour["GLOBALS"].append([value])
            elif key.startswith('INSTANCE'):
                retour["GLOBALS"].append(value)
            else:
                raise MappingException("GLOBALS child must be either COLLECTION or GLOBALS ({} prohibited".format(key))
            
        DictUtils.print_pretty_json(retour["GLOBALS"])
        import sys
        sys.exit(1)
           
        globals_block = json_block['VODML']['TEMPLATES']
        for item in globals_block:
            table_ref = item[ "@tableref"]
            retour["TEMPLATES"][table_ref] = {"WHERE":[], "ITEMS":[]}
            item.pop("@tableref")
            
            for key, subitem in item.items():
                if key == "WHERE":
                    retour["TEMPLATES"][table_ref]["WHERE"].append(subitem)
                elif key.startswith("INSTANCE"):
                    retour["TEMPLATES"][table_ref]["ITEMS"].append(subitem)
                    subitem.pop("@dmrole")
                else:
                    raise MappingException("TEMPLATES child must be either WHERE or INSTANCE ({} prohibited".format(key))

        DictUtils.print_pretty_json(retour["GLOBALS"])

        json_mapping_builder = JsonMappingBuilder(json_dict=retour)
        revert_coll = JsonBlockExtractor.search_array_container(retour, "COLLECTION")
        for item in revert_coll:
            item["host"][item["content"]["@dmrole"]]  = {"ITEMS":[]} 
            coll_mapping = item["host"][item["content"]["@dmrole"]]
            for key, value in item["content"].items():
                if key == "REFERENCE":
                    coll_mapping["REFERENCE"] = value
                elif key == "JOIN":
                    coll_mapping["JOIN"] = value
                elif key != '@dmrole':
                    coll_mapping["ITEMS"].append(value)
                    
            item["host"].pop(item["key"])
            

        #json_mapping_builder.proto_revert_collections()
        #json_mapping_builder.proto_revert_elements("INSTANCE")
        print("==============")
        #DictUtils.print_pretty_json(json_mapping_builder.json)

        revert_obj = JsonBlockExtractor.search_object_container(retour, "ATTRIBUTE")        
        for item in revert_obj:
            item["host"][item["content"]["@dmrole"]]  = item["content"]
            item["host"].pop(item["key"])
            item["content"].pop('@dmrole', None)
            
            
        DictUtils.print_pretty_json(json_mapping_builder.json)

        #revert_coll = JsonBlockExtractor.search_object_container(retour, "INSTANCE")
       
        
        return json_mapping_builder.json

        

    
    
    