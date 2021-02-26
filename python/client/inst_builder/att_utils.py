'''
Created on Jul 6, 2020

@author: laurentmichel
'''


class AttUtils(object):
    """
    Some static methods doing tests on JSON mapping elements 
    """

    @staticmethod 
    def id_matches(element, searched_id):     
        """
        Returns True if element[@ID] matches id
        """
        if(isinstance(element, dict) and 
            "@ID" in element.keys() and 
            element["@ID"] == searched_id):
            return True
        return False
    
    @staticmethod 
    def type_matches(element, searched_type):
        """
        Returns True if element[@dmtype] matches searched_type
        """
        if(isinstance(element, dict) and 
            "@dmtype" in element.keys() and 
            element["@dmtype"] == searched_type):
            return True
        return False
    
    @staticmethod 
    def is_object_ref(element):
        """
        Returns True if the element is an object reference
        <INSTANCE dmref=xxx/>
        """
        if(isinstance(element, dict) and 
            "@dmref" in element.keys() and 
            "@dmtype" not in element.keys()):
            return True
        return False
