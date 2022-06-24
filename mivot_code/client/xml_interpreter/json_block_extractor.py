'''
Created on Jul 6, 2020

@author: laurentmichel
'''
from mivot_code.client.xml_interpreter.vocabulary import key_match
from mivot_code.client.xml_interpreter.att_utils import AttUtils
class JsonBlockExtractor(object):
    '''
    Block search utilities in dicts resulting from the xml2dict conversion of the mapping block
    This class is just a name space for a set of functions (static method) independent to each other.
    This private methods (starting with _) are not meant to be used out of the scope of that class. 
    
    The search function are recursive
    search_object_container and search_object_container return lists of dictionaries where 
    all searched components are exposed in a convenient way.
    example:  
        we search for INSTANCE object in in the following sequence
            INSTANCE:{role, type, ATTRIBUTE{role1, type1}, INSTANCE: {role2, type2}}
        then we get the following result:
            [
             {key:INSTANCE, 
              content: {role2, type2}, 
              host:{role, type, ATTRIBUTE{role1, type1}, INSTANCE: {role2, type2}}
             ]
    This structure facilitates either the modification of the replacement of the searched objects directly into the tree.
    
    In some cases (JOIN, REFERENCE), the keys of the searched objects are not known due to a former processing (numbering appended), 
    this is why the key identification are done by the key_match function
    '''
                                
    @staticmethod    
    def search_subelement_by_type(json_block, searched_type):
        '''
        Returns the list of all object haveing the searched type.
        It is to noted that the returned list is flat, there is no information about the searched object contexts. 
        :param json_block: Block where to search in 
        :param searched_type: searched @dmtype
        '''
        searched_elements = []
        JsonBlockExtractor._search_subelement_by_type(json_block, searched_type, searched_elements)
        return searched_elements
    
    @staticmethod    
    def search_subelement_by_role(json_block, searched_role):
        '''
        Returns the list of all object haveing the searched type.
        It is to noted that the returned list is flat, there is no information about the searched object contexts. 
        :param json_block: Block where to search in 
        :param searched_type: searched @dmtype
        '''
        searched_elements = []
        JsonBlockExtractor._search_subelement_by_key(json_block, searched_role, searched_elements)
        return searched_elements
    
    @staticmethod    
    def search_object_container(root_element, element_key):
        '''
        Return a [{key, content, host}...] list with all objects ({...}) contained in root_element 
        :param root_element: Block where to search in 
        :param element_key: key of the searched object
        '''
        searched_elements = []
        JsonBlockExtractor._search_object_container(root_element, element_key, searched_elements)
        return searched_elements
    
    @staticmethod    
    def search_array_container(root_element, element_key):
        '''
        Return a [{key, content, host}...] list with all lists ([...]) contained in root_element 
        :param root_element: Block where to search in 
        :param element_key: key of the searched object
        '''
        searched_elements = []
        JsonBlockExtractor._search_array_container(root_element, element_key, searched_elements)
        return searched_elements

    @staticmethod    
    def _search_array_container(root_element, element_key, searched_elements):
        """
        Recursive function searching arrays
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                item = root_element[idx]
                if isinstance(item, dict) and key_match(element_key,item.keys()) is not None:
                    searched_elements.append({"key": key_match(element_key,idx.keys()), 
                                              "content": item, "host": root_element})
                JsonBlockExtractor._search_array_container(item, element_key, searched_elements)
        elif isinstance(root_element, dict):
            for _, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:

                        if isinstance(ele, dict) and key_match(element_key,ele.keys()) is not None:
                            matching_key = key_match(element_key,ele.keys())
                            searched_elements.append({"key": matching_key, 
                                                      "content": ele[matching_key], 
                                                      "host": ele})
                            # if one matching element is found in a array, the whole
                            # array content will be stored.
                            # if we parse the others items, we might have result duplication
                            break
                        JsonBlockExtractor._search_array_container(ele, element_key, searched_elements)
                elif isinstance(v, dict):  
                    JsonBlockExtractor._search_array_container(v, element_key, searched_elements)
 
    @staticmethod
    def _search_object_container(root_element, element_key, searched_elements):
        """
        Recursive function searching objects
        """
        if isinstance(root_element, list):
            for item in root_element:
                if isinstance(item, dict):  
                    JsonBlockExtractor._add_object_in_searched_elements(item, element_key, searched_elements)
                JsonBlockExtractor._search_object_container(item, element_key, searched_elements)
        elif isinstance(root_element, dict):
            for _, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        if isinstance(ele, dict):
                            JsonBlockExtractor._add_object_in_searched_elements(ele, element_key, searched_elements)
                                    
                        JsonBlockExtractor._search_object_container(ele, element_key, searched_elements)
                elif isinstance(v, dict):  
                    JsonBlockExtractor._add_object_in_searched_elements(v, element_key, searched_elements)

                            
                        #JsonBlockExtractor._search_object_container(value,element_key,  searched_elements)
                    JsonBlockExtractor._search_object_container(v,element_key,  searched_elements)
                   
    @staticmethod
    def _add_object_in_searched_elements(instance, element_key, searched_elements):
        """
        build a response item {key, content, host}
        """
        for key, value in instance.items():
            if key.startswith('@') is True:
                continue
            if key_match(element_key,[key]) is not None:
                matching_key = key_match(element_key,[key])
                searched_elements.append({"key": matching_key, 
                                          "content": value, 
                                          "host": instance})


 
    def _search_subelement_by_role(self, root_element, searched_role):
        """
        Store in self.searched_elements all elements with @dmrole=searched_role
        Recursive search
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    self._search_subelement_by_role(root_element[idx], searched_role)
        elif isinstance(root_element, dict):
            for k, v in root_element.items():
                if k == searched_role:
                    self.searched_elements.append(v)
                if isinstance(v, list):
                    for ele in v:
                        self._search_subelement_by_role(ele, searched_role)
                elif isinstance(v, dict):  
                    self._search_subelement_by_role(v, searched_role)
                    
    @staticmethod
    def _search_subelement_by_key(root_element, searched_key,  searched_elements):
        """
        Store in self.searched_elements all elements attached to the key searched_key
        used for search by role
        Recursive search
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                JsonBlockExtractor._search_subelement_by_key(root_element[idx], searched_key,  searched_elements)
        elif isinstance(root_element, dict):
            for k, v in root_element.items():
                if k == searched_key  :
                    searched_elements.append(v)
                if isinstance(v, list):
                    for ele in v:
                        JsonBlockExtractor._search_subelement_by_key(ele, searched_key,  searched_elements)
                elif isinstance(v, dict):  
                    JsonBlockExtractor._search_subelement_by_key(v, searched_key,  searched_elements)

    @staticmethod
    def _search_subelement_by_id(root_element, searched_id, searched_elements):
        """
        Store in self.searched_ids all elements with @ID=searched_id
        Recursive search
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if AttUtils.id_matches(root_element[idx], searched_id):
                    searched_elements.append(root_element[idx])
                JsonBlockExtractor._search_subelement_by_id(root_element[idx], searched_id, searched_elements)
        elif isinstance(root_element, dict):
            if AttUtils.id_matches(root_element, searched_id):
                searched_elements.append(root_element) 
            for _, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        if AttUtils.id_matches(ele, searched_id):
                            pass
                            #searched_elements.append(ele)
                        JsonBlockExtractor._search_subelement_by_id(ele, searched_id, searched_elements)
                elif isinstance(v, dict):  
                    if AttUtils.id_matches(v, searched_id):
                        pass
                        #searched_elements.append(v)
                    JsonBlockExtractor._search_subelement_by_id(v, searched_id, searched_elements)

    @staticmethod
    def _search_subelement_by_type(root_element, searched_type, searched_elements):
        """
        Store in self.searched_types all elements with @dmtype=searched_type
        Recursive search
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if AttUtils.type_matches(root_element[idx], searched_type):
                    searched_elements.append(root_element[idx])
                JsonBlockExtractor._search_subelement_by_type(root_element[idx], searched_type, searched_elements)
        elif isinstance(root_element, dict):
            if AttUtils.type_matches(root_element, searched_type):
                searched_elements.append(root_element) 
            for _, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        if AttUtils.type_matches(ele, searched_type):
                            pass
                            #self.searched_elements.append(ele)
                        JsonBlockExtractor._search_subelement_by_type(ele, searched_type, searched_elements)

                elif isinstance(v, dict):  
                    if AttUtils.type_matches(v, searched_type):
                        pass
                        #self.searched_elements.append(v)
                    JsonBlockExtractor._search_subelement_by_type(v, searched_type, searched_elements)
    @staticmethod
    def __set_column_indices(mapping_block, index_map):
        """
        add column ranks to attribute having a ref.
        Using ranks allow to identify columns even numpy raw have been serialised as []
        """
        print(index_map)
        for ele in mapping_block.xpath("//ATTRIBUTE"):
            ref = ele.get("ref")
            print(f'{ele.get("dmrole")} {ele.get("ref")}')
            if ref is not None and ref != 'NotSet':
                print(f"good {index_map[ref]}")
                ele.attrib["index"] = str(index_map[ref])
                
    @staticmethod
    def _set_column_units(mapping_block, unit_map):
        """
        add field unit to attribute having a ref.
        Used for performing unit conversions
        """
        for ele in mapping_block.xpath("//ATTRIBUTE"):
            ref = ele.get("ref")
            if ref is not None and ref != 'NotSet':
                unit = unit_map[ref]
                if unit is None:
                    unit = ""
                else:
                    unit = unit.__str__()
                ele.attrib["unit_org"] = unit


