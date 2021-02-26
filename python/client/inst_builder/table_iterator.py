'''
Created on 1 avr. 2020

@author: laurentmichel
'''
from copy import deepcopy


class TableIterator(object):
    '''
    classdocs
    '''

    def __init__(self,
                 name,
                 data_table,
                 array_mapping_block,
                 column_mapping,
                 row_filter=None):
        '''
        Constructor
        '''
        self.name = name
        self.data_table = data_table
        self.column_mapping = column_mapping
        self.row_filter = row_filter
        self.last_row = None
        if isinstance(array_mapping_block, list):
            self.array_mapping_block = array_mapping_block[0]
        else:
            self.array_mapping_block = array_mapping_block

        self.iter = None
       
    def __repr__(self):
        return "name={} column_mapping={} row_filter={}".format(self.name , self.column_mapping, self.row_filter)
    
    def _get_row_subelement(self, root_element, row):
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    self._get_row_subelement(root_element[idx], row)
        elif isinstance(root_element, dict):
            for k , v in root_element.items():
                # JOIN content is processed by join_iterator
                if k == 'JOIN':
                    return
                if isinstance(v, list):
                    for ele in v:
                        self._get_row_subelement(ele, row)
                elif isinstance(v, dict):  
                    self._set_row_value(v, row)
                    self._get_row_subelement(v, row)
    
    def _set_row_value(self, element, row):
        keys = element.keys()
        if ("@dmtype" in keys and "@ref" in keys 
            and "@value" in keys):  # and element["@value"] == "array coucou"):
            val = row[self.column_mapping.get_index(element['@ref'])]
            if isinstance(val, bytes) is True:
                    val = val.decode("UTF-8")
            element['@value'] = val

    def _get_next_row(self):
        if self.iter == None:
            self.iter = iter(self.data_table)
            if self.row_filter is not None:
                self.row_filter.map_col_number(self.column_mapping)

        try:
            while True:
                row = next(self.iter)
                if row is not None:
                    if (self.row_filter is None or 
                        self.row_filter.row_match(row) == True):
                        self.last_row = row
                        return row
                else:
                    return None
        except:  
            # traceback.print_exc()    
            return None

    def _rewind(self):
        self.iter = None
        
    def _get_next_row_instance(self):
        row = self._get_next_row()
        if row is not None:
            self._get_row_subelement(self.array_mapping_block, row) 
            return deepcopy(self.array_mapping_block)
        else:
            return None

    def _get_next_flatten_row(self):
        row = self._get_next_row()
        if row is not None:
            retour = []
            indexes = self.column_mapping.get_indexes()
            for index in indexes:
                val = row[index]
                if isinstance(val, bytes) is True:
                    val = val.decode("UTF-8")
                retour.append(val)
            return retour 
        else:
            return None

    def _get_flatten_data_head(self):
        return self.column_mapping.get_column_head()
