'''
Created on 7 Nov 2021

@author: laurentmichel
'''

class ResourceSeeker(object):
    '''
    TODO At the time of writing the class is static in order to be callable from any part of the code.
    This feature should be made thread-safe in a public release
    '''
    votable_path = None
    votable = None
    
    def __init__(self, resource):
        self._resource = resource
            
    def get_table_ids(self):
        """
        Return the list of table ids
        Only resource children are considered
        The id is first look up in ID then in name and finally 'AnonymousTable' is taken
        """
        retour = []
        for table in self._resource.tables:
            if table.ID is not None:
                retour.append(table.ID)
            elif table.name is not None:
                retour.append(table.name)
            else:
                retour.append('AnonymousTable')
        return retour
       
    
    def get_table(self, table_name):
        '''
        Returns the table matching table_name first by ID and the by name
        :param table_name:
        '''
        for table in self._resource.tables:
            if (table_name is None or table.name == table_name 
                or table.ID == table_name):
                return table
        return None
    
    def get_params(self):
        '''
        returns the VOTable PARAMS
        '''
        return self._resource.params
    
    def get_id_index_mapping(self, table_name):
        '''
        build an index binding colum number with field id
        :param table_name: name of the table
        '''
        retour = {}
        table = self.get_table(table_name)   
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

    def get_id_unit_mapping(self, table_name):
        '''
        build an index binding filed unit with field id
        :param table_name: name of the table
        '''
        retour = {}
        table = self.get_table(table_name)   
        for field in  table.fields:
            unit = field.unit
            if field.ID is not None:
                retour[field.ID] = unit
            elif field.name is not None:
                retour[field.name] = unit
            elif field.ref is not None :
                retour[field.ref] = unit
        return retour

