'''
Created on 7 Nov 2021

@author: laurentmichel
'''
from astropy.io.votable import parse

class VOTablePointer(object):
    '''
    classdocs
    '''
    votable_path = None
    votable = None
    @staticmethod 
    def connect(votable_path):
        '''
        Constructor
        '''
        VOTablePointer.votable_path = votable_path
        VOTablePointer.votable = parse(votable_path)
        
    @staticmethod 
    def get_table(table_name):
        '''
        Returns the table matching table_name first by ID and the by name
        :param table_name:
        '''
        for resource in VOTablePointer.votable.resources:
            if resource.type == "results":
                for table in resource.tables:
                    if (table_name is None or table.name == table_name 
                        or table.ID == table_name):
                        return table
        return None
    
    @staticmethod 
    def get_params():
        '''
        returns the VOTable PARAMS
        '''
        return VOTablePointer.votable.params
    
    
    @staticmethod 
    def get_id_index_mapping(table_name):
        '''
        build an index binding colum number with field id
        :param table_name: name of the table
        '''
        retour = {}
        table = VOTablePointer.get_table(table_name)   
        indx = 0     
        for field in  table.fields:
            if field.ID is not None:
                retour[field.ID] = indx
            elif field.name is not None:
                retour[field.name] = indx
            elif field.ref is not None :
                retour[field.ref] = indx
            indx += 1
        return retour

