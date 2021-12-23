'''
Created on Jul 6, 2020

@author: laurentmichel
'''

from client.translator.vocabulary import Ele, Att


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
            Att.dmid in element.keys() and 
            element[Att.dmid] == searched_id):
            return True
        return False
    
    @staticmethod 
    def type_matches(element, searched_type):
        """
        Returns True if element[@dmtype] matches searched_type
        """
        if(isinstance(element, dict) and 
            Att.dmtype in element.keys() and 
            element[Att.dmtype] == searched_type):
            return True
        return False
    
