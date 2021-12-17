'''
Created on 11 Dec 2021

@author: laurentmichel
'''
from client.objectbuilder.mapping_exception import MappingException
from client.translator.vocabulary import Att, Ele
from client.translator import logger
import xmltodict, lxml
from utils.dict_utils import DictUtils
from client.translator.json_mapping_builder import JsonMappingBuilder
from client.objectbuilder.json_block_extractor import JsonBlockExtractor

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
                
        for tag in['INSTANCE', 'ATTRIBUTE', 'COLLECTION']:
            cpt=1
            xpath = './/dm-mapping:' + tag
            
            for ele in MappingBlockCursor._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag + "_" + str(cpt)
                cpt += 1
                
        for tag in['GLOBALS', 'TEMPLATES', 'REFERENCE', 'JOIN', 'PRIMARY_KEY', 'FOREIGN_KEY', 'WHERE', 'VODML']:
            xpath = '//dm-mapping:' + tag            
            for ele in MappingBlockCursor._xml_block.xpath(xpath, namespaces=xml_block.nsmap):
                ele.tag = tag 
            
        

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
    def get_templates_blocks():
        pass                 
    
    @staticmethod    
    def get_globals_collection(dmid):
        pass                 

    @staticmethod    
    def get_globals_object(dmtype):
        pass                 
   
    @staticmethod    
    def get_templates(tableref):
        pass                 
    
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

        

    
    
    