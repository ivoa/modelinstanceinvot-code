'''
Created on 13 sept. 2021

@author: michel
'''
import re
from copy import deepcopy
from client import logger
from client.objectbuilder.json_block_extractor import JsonBlockExtractor
from client.objectbuilder.att_utils import AttUtils
from client.translator.vocabulary import Att, Ele
from builtins import staticmethod
class ReferenceResolver(object):
    '''
    classdocs
    '''
    @staticmethod
    def resolve_object_references(json_block):
        #
        # resolve object reference
        # an object reference is something like {"@ref"=xxx}
        # Refrences are replaced with copies of object looking like
        #  {"@ID"=xxx ...}
        #
        root = json_block
        while True:
            replacement_list = []  

            ReferenceResolver._get_object_references(root, replacement_list)

            if len(replacement_list) == 0:
                break
            else :
                for replacement in replacement_list:
                    ReferenceResolver._resolve_references(root, replacement)
    
    @staticmethod
    def _resolve_references(root, replacement):        
        tempo = ReferenceResolver._search_instance_by_id(replacement["dmref"], root)
        if len(tempo) == 0:
            logger.warning("Cannot resolve dm reference %s",replacement["dmref"] )
            return
        else:
            instance = ReferenceResolver._search_instance_by_id(replacement["dmref"], root)[0]
            # ref instance is an array element: decode the rank
            logger.info("resolve dm reference %s", replacement["dmref"])
            if replacement["key"].startswith("#"):
                col_num = int(re.search(r'^#([\d]+).*$', replacement["key"]).group(1))
                replacement["node"][col_num] = deepcopy(instance)
            else:
                role = replacement["node"][replacement["key"]][Att.dmrole]
                replacement["node"].pop(replacement["key"]) 
                replacement["node"][role] = deepcopy(instance) 
    
    
    @staticmethod
    def _get_object_references(root_element, replacement_list):
        """
        recursive function
        Looks into root_element for element being references (INSTANCE with @dmref)
        Objects found are stored in replacement_list
        
        :param root_element: Root element for the search
        :type root_element: XML element
        :param replacement_list: List of the found elements
        :type replacement_list: list of {"node": element found, "key": role if the reference, "dmref": instance reference}
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                ReferenceResolver._get_object_references(root_element[idx], replacement_list)
        elif isinstance(root_element, dict):
            for k , v in root_element.items():
                if isinstance(v, list):
                    cpt=0
                    for ele in v:
                        # if the array item is a rank is encoded in the key
                        if AttUtils.is_object_ref(ele):
                            replacement_list.append(
                            {"node": v,
                             "key": "#" + str(cpt) + " " + k,
                             "dmref": ele[Att.dmref]}
                            )
                        cpt += 1
                        ReferenceResolver._get_object_references(ele, replacement_list)
                elif isinstance(v, dict):  
                    if AttUtils.is_object_ref(v):
                        replacement_list.append(
                            {"node": root_element,
                             "key": k,
                             "dmref": v[Att.dmref]})
                    ReferenceResolver._get_object_references(v, replacement_list)
                            
    @staticmethod
    def _search_instance_by_id(searched_id, root_element):
        root = root_element
        json_block_extractor = JsonBlockExtractor(root)
        return json_block_extractor.search_subelement_by_id(searched_id)
 