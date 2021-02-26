'''
Created on 26 mars 2020

@author: laurentmichel
'''
import json
from copy import deepcopy
from client.inst_builder import logger
from utils.dict_utils import DictUtils
from client.translator.json_tools import JsonTools


class JsonMappingBuilder():
    '''
    classdocs
    '''

    def __init__(self, json_path=None, json_dict=None):
        '''
        Constructor
        '''
        if  json_path is not None:
            self.json_path = json_path
            with open(json_path) as json_file:
                self.json = json.load(json_file)
        else:
            self.json = json_dict
            self.json_path = None
    
    def revert_templates(self):  
        logger.info("reverting templates - {TABLE_MAPPING:[{ref_table ...} ] -> 'ref_table':{...}")
        
        self.revert_elements("TABLE_MAPPING")
        root_element = self.json['MODEL_INSTANCE']
        templates = {}
        keys = []
        for k, v in  root_element.items():
            if k not in ['MODELS', 'GLOBALS'] and k.startswith("@") is False:
                templates[k] = v
                keys.append(k)
        logger.info("Put all TABLE_MAPPING{} in a global TABLE_MAPPING[]")
       
        for  k in keys:
            root_element.pop(k)
        
        root_element["TABLE_MAPPING"] = templates

    def revert_elements(self, name, dmrole=None, dmtype=None):
        logger.info("reverting elements %s - ('%s':{role ...} -> 'role':{})", name, name)
        root_element = self.json['MODEL_INSTANCE']
        while True:
            self.retour = None
            self._revert_subelement(root_element, name, dmrole, dmtype)
            if self.retour is not None:
                self.retour["node"].pop(name)
                for k, v in self.retour["newcontent"].items():
                    self.retour["node"][k] = v
            else:
                break
            
    def revert_compositions(self, name, dmrole=None, dmtype=None):
        logger.info("reverting compositions %s - ('%s':[{role ...} ...] -> 'role':[...])", name, name)

        root_element = self.json['MODEL_INSTANCE']
        while True:
            self.retour = None
            self._revert_composition(root_element, name, dmrole, dmtype)
            if self.retour is not None:
                self.retour["node"].pop(name)

                for ele in self.retour["newcontent"]:
                    for k, v in ele.items():
                        self.retour["node"][k] = JsonTools.remove_key(v, "INSTANCE")
            else:
                break
                       
    def _revert_subelement(self, root_element, name, dmrole, dmtype):
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    self._revert_subelement(root_element[idx], name, dmrole, dmtype)
        elif isinstance(root_element, dict):
            for k, v in root_element.items():
                if k == name:
                    if isinstance(v, list):
                        # print(DictUtils.get_pretty_json(v))
                        '''
                        newcontent = {}
                        ele_array = []
                        for ele in v:
                            new_key = self._get_key_for_element(ele)

                            new_ele  = deepcopy(ele)
                            self._drop_role_if_needed(new_ele)
                            self._add_value_if_needed(new_ele)
                            ele_array.append(new_ele)
                            
                        newcontent[new_key] = deepcopy(ele_array)
                        '''
                        # if we got an array of objects with all the same role
                        # we have a composition of instances. In that case that
                        # role is given the composition object and to object array 
                        # is given as the composition content
                        former_key = ""
                        is_array = True
                        for ele in v:
                            new_key = self._get_key_for_element(ele)
                            if former_key == "":
                                former_key = new_key
                            if former_key != new_key:
                                is_array = False
                                break 
                        if is_array is False:
                            newcontent = {}
                            for ele in v:
                                new_key = self._get_key_for_element(ele)
                                new_ele = deepcopy(ele)
                                self._drop_role_if_needed(new_ele)
                                self._add_value_if_needed(new_ele)                            
                                newcontent[new_key] = new_ele
                        else:
                            logger.info("find a composition of %s with the role=%s", name, former_key)
                            newcontent = {}
                            new_array = []
                            for ele in v:
                                new_ele = deepcopy(ele)
                                # self._drop_role_if_needed(new_ele)
                                self._add_value_if_needed(new_ele)    
                                new_array.append(new_ele)
                            newcontent[former_key] = new_array
                        
                        self.retour = {'node': root_element, "newcontent": newcontent}
                    elif isinstance(v, dict):  
                        newcontent = {}
                        new_key = self._get_key_for_element(v)
                        newcontent[new_key] = deepcopy(v)
                        self._add_value_if_needed(newcontent[new_key])
                        self._drop_role_if_needed(newcontent[new_key])
                        self.retour = {'node': root_element, "newcontent": newcontent}

                if self.retour is None:
                    self._revert_subelement(v, name, dmrole, dmtype)
                    
    def _revert_composition(self, root_element, name, dmrole, dmtype):
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    self._revert_composition(root_element[idx], name, dmrole, dmtype)
        elif isinstance(root_element, dict):
            for k, v in root_element.items():
                if k == name:

                    if isinstance(v, list):
                        newcontent = []
                        for ele in v:
                            new_key = self._get_key_for_element(ele)
                            ele_cp = deepcopy(ele)
                            self._drop_role_if_needed(ele_cp)
                            if ele_cp:
                                newcontent.append({new_key: [ele_cp]})
                            else :
                                # print("Append 1 empty" )
                                newcontent.append({new_key: []})
                        self.retour = {'node': root_element, "newcontent": newcontent}
                    elif isinstance(v, dict):  

                        newcontent = []
                        ele_cp = deepcopy(v)
                        new_key = self._get_key_for_element(ele_cp)
                        self._drop_role_if_needed(ele_cp)

                        if ele_cp:
                            newcontent.append({new_key: [ele_cp]})
                        else :
                            newcontent.append({new_key: []})

                        self.retour = {'node': root_element, "newcontent": newcontent}

                if self.retour is None:
                    self._revert_composition(v, name, dmrole, dmtype)
                    
    def _add_value_if_needed(self, element):
        keys = element.keys()
        if  "@dmtype" in keys and "@ref" in keys and "@value" not in keys:
            element["@value"] = ""
    
    def _drop_role_if_needed(self, element):
        keys = element.keys()
        if  "@dmrole" in keys :
            element.pop("@dmrole")   
        if  "@size" in keys :
            element.pop("@size")   
                            
    def _get_key_for_element(self, element, default_key=None):
        if default_key is not None:
            return default_key
        new_key = ''
        if "@dmrole" in element.keys():
            new_key = element["@dmrole"]
        if "@tableref" in element.keys():
            new_key = element["@tableref"]
        if new_key == '' and "@ID" in element.keys():
            new_key = element["@ID"]
        if new_key == '' and "NAME" in element.keys():
            new_key = element["NAME"]
        if new_key == '':
            raise Exception("Cannot compute new key (from dmrole, tableref, ID or NAME) for element " + DictUtils.get_pretty_json(element))
        return new_key
   
    def save_instance(self):     
        file_path = self.json_path.replace(".json", ".inst.json")
        logger.info("save instance in %s", file_path)   
        with open(file_path, 'w') as jsonfile:
            jsonfile.write(DictUtils.get_pretty_json(self.json))
