'''
Created on March 2, 2021
Straight access to dict instances

@author: laurentmichel
'''


class InstanceBrowser(object):
    '''
    Provides a few methods helping for browsing JSON serialization of a mapping block
    '''

    def __init__(self, json_instance):
        '''
        Constructor
        :param json_instance: JSON serialization of the mapping block
        :type json_instance: dict 
        '''
        self.json_instance = json_instance
        self.__valid_json_instance()
    
    def __valid_json_instance(self):
        """
        Operate a basic validation on the JSON serialization of the mapping block
        Just what is required for the public methods not to fail
        """
        if "MODEL_INSTANCE" not in self.json_instance:
            raise KeyError("mapping instance has no 'MODEL_INSTANCE'")
        
        if "GLOBALS" not in self.json_instance["MODEL_INSTANCE"]:
            raise KeyError("'MODEL_INSTANCE' has no 'GLOBALS'")
        
        if "TABLE_MAPPING" not in self.json_instance["MODEL_INSTANCE"]:
            raise KeyError("'MODEL_INSTANCE' has no 'TABLE_MAPPING'")
        
        
    def get_globals_types(self):
        """
        :return : the list of the dmtypes of the GLOBALS children
        :rtype : [string]
        """
        retour  = []
        for key in self.json_instance["MODEL_INSTANCE"]["GLOBALS"].keys():
            retour.append(self.json_instance["MODEL_INSTANCE"]["GLOBALS"][key]["@dmtype"])
        return retour

    def get_globals_by_type(self, dmtype):
        """
        :return: the first GLOBALS child with @dmtype = type of None is nothing found
        :rtype: dict.
        """
        for key in self.json_instance["MODEL_INSTANCE"]["GLOBALS"].keys():
            if dmtype == self.json_instance["MODEL_INSTANCE"]["GLOBALS"][key]["@dmtype"]:
                return self.json_instance["MODEL_INSTANCE"]["GLOBALS"][key]
        return None
    
    def get_globals_by_ID(self, ID):
        """
        :return: the first GLOBALS child with @dmtype = type of None is nothing found
        :rtype: dict.
        """
        for key in self.json_instance["MODEL_INSTANCE"]["GLOBALS"].keys():
            if "@ID" in self.json_instance["MODEL_INSTANCE"]["GLOBALS"][key].keys() and ID == self.json_instance["MODEL_INSTANCE"]["GLOBALS"][key]["@ID"]:
                return self.json_instance["MODEL_INSTANCE"]["GLOBALS"][key]
        return None
        
    def get_root_element(self):
        """
        :return: the first TABLE_MAPPING child with @dmrole = "root" of None is nothing found
        :rtype: dict.
        TODO: conflict with VodmlInstance.get_root_element()
        """
        for key in self.json_instance["MODEL_INSTANCE"]["TABLE_MAPPING"].keys():
            if "root" in self.json_instance["MODEL_INSTANCE"]["TABLE_MAPPING"][key].keys():
                return self.json_instance["MODEL_INSTANCE"]["TABLE_MAPPING"][key]["root"]
        return None
    
    def get_root_component_roles(self):
        """
        Get the roles of all children of the first root element found.
        The roles are identified  as JSON keys not starting with @
        JSON keys starting with @ are object attribute (e.g. @dmtype)
        :return : role list
        :rtype: [string]
        """
        retour  = []
        for key in self.get_root_element().keys():
            if key.startswith("@") is False:
                retour.append(key)
        return retour
    
    def get_root_component_by_role(self, dmrole):
        """
        Get the child of the first root element found with a role = dmrole
        :param dmrole: searched role
        :type dmrole: string
        :return : searched element
        :rtype: dict
        """
        for key in self.get_root_component_roles():
            if key == dmrole:
                return self.get_root_element()[key]
        return None

