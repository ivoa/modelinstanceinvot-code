'''
Created on 1 avr. 2020

@author: laurentmichel
'''
from copy import deepcopy
from utils.json_tools import JsonTools
from client.translator.vocabulary import Att, Ele
from utils.dict_utils import DictUtils
class TableIterator(object):
    '''
    classdocs
    '''

    def __init__(self,
                 name,
                 data_table):
        '''
        Constructor
        '''
        self.name = name
        self.data_table = data_table
        self.last_row = None
        self.iter = None
        self.row_filter = None

    def _get_next_row(self):
        if self.iter == None:
            self.iter = iter(self.data_table)
            if self.row_filter is not None:
                pass
                #print(self.row_filter)
                #self.row_filter.map_col_number(self.column_mapping)
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
            return None

    def _rewind(self):
        self.iter = None
        
 
