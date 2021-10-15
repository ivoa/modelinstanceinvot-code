'''
Created on Jul 6, 2020

@author: laurentmichel
'''
from client.translator.vocabulary import Ele, Att
from client.objectbuilder.att_utils import AttUtils


class JsonBlockExtractor(object):
    '''
    Search utilities blocks in dicts  resulting from the xml2dict conversion of the mapping block
    '''

    def __init__(self, json_block):
        '''
        Constructor
        :param json_block: Dict resulting from the xml2dict conversion of the mapping block
        :param type: {}
        '''
        self.json_block = json_block

        # Buffer storing the search results
        # Result cannot be returned direclty because search functions are recursives
        self.searched_elements = []
        
    def search_table_row_template_container(self):
        self._search_array_container("TABLE_ROW_TEMPLATE", self.json_block)
        return self.searched_elements
        
    def search_elment_by_key(self, key):
        self._search_array_container(key, self.json_block)
        return self.searched_elements
        
    def search_join_container(self):
        self._search_array_container(Ele.JOIN, self.json_block)
        return self.searched_elements

    def search_subelement_by_role(self, searched_role):
        self._search_subelement_by_role(self.json_block, searched_role)
        return self.searched_elements
        
    def search_subelement_by_id(self, searched_id):
        self._search_subelement_by_id(self.json_block, searched_id)
        return self.searched_elements
    
    def search_subelement_by_type(self, searched_type):
        self._search_subelement_by_type(self.json_block, searched_type)
        return self.searched_elements
        
    def _search_array_container(self, element_name, root_element):
        """
        Recursive search in root_element of all list that have at least 
        one item named (dict key) element_name
        The list contents are packed in self.searched_elements.
        By construction self.searched_elements is a [[]]
        See unittest 
        :param element_name: name of the searched element 
        :type element_name: string
        :param   root_element: element to be explored
        :type root_element : {} or [] 
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                item = root_element[idx]
                if isinstance(item, dict) and element_name in item.keys():
                    self.searched_elements.append(root_element)
                self._search_array_container(element_name, item)
        elif isinstance(root_element, dict):
            for _, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        if isinstance(ele, dict) and element_name in ele.keys():
                            self.searched_elements.append(v)
                            # if one matching element is found in a array, the whole
                            # array content will be stored.
                            # if we parse the others items, we might have result duplication
                            break
                        self._search_array_container(element_name, ele)
                elif isinstance(v, dict):  
                    self._search_array_container(element_name, v)


    def _search_array_container_2(self, element_name, root_element):
        """
        TODO rename and comment
        :param element_name: name of the searched element 
        :type element_name: string
        :param   root_element: element to be explored
        :type root_element : {} or [] 
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                item = root_element[idx]
                self._search_array_container_2(element_name, item)
        elif isinstance(root_element, dict):
            for k, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        if isinstance(ele, dict) and element_name in ele.keys():
                            self.searched_elements.append({"key": k, "node": root_element})
                            # if one matching element is found in a array, the whole
                            # array content will be stored.
                            # if we parse the others items, we might have result duplication
                            break
                        self._search_array_container_2(element_name, ele)
                elif isinstance(v, dict):  
                    self._search_array_container_2(element_name, v)
 
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

    def _search_subelement_by_id(self, root_element, searched_id):
        """
        Store in self.searched_ids all elements with @ID=searched_id
        Recursive search
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    if self._id_matches(root_element[idx], searched_id):
                        self.searched_elements.append(root_element[idx])
                    self._search_subelement_by_id(root_element[idx], searched_id)
        elif isinstance(root_element, dict):
            if AttUtils.id_matches(root_element, searched_id):
                self.searched_elements.append(root_element) 
            for _, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        if AttUtils.id_matches(ele, searched_id):
                            self.searched_elements.append(ele)
                        self._search_subelement_by_id(ele, searched_id)
                elif isinstance(v, dict):  
                    if AttUtils.id_matches(v, searched_id):
                        self.searched_elements.append(v)
                    self._search_subelement_by_id(v, searched_id)

    def _search_subelement_by_type(self, root_element, searched_type):
        """
        Store in self.searched_types all elements with @dmtype=searched_type
        Recursive search
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    if self._type_matches(root_element[idx], searched_type):
                        self.searched_elements.append(root_element[idx])
                    self._search_subelement_by_type(root_element[idx], searched_type)
        elif isinstance(root_element, dict):
            if AttUtils.type_matches(root_element, searched_type):
                self.searched_elements.append(root_element) 
            for _, v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        if AttUtils.type_matches(ele, searched_type):
                            self.searched_elements.append(ele)
                        self._search_subelement_by_type(ele, searched_type)
                elif isinstance(v, dict):  
                    if AttUtils.type_matches(v, searched_type):
                        self.searched_elements.append(v)
                    self._search_subelement_by_type(v, searched_type)
