'''
Created on 18 Nov 2021

@author: laurentmichel
'''
from utils.json_tools import JsonTools
from utils import logger
from client.translator.vocabulary import Att, Ele
from client.objectbuilder.column_mapping import ColumnMapping
from client.objectbuilder.table_iterator import TableIterator
from client.objectbuilder.votable_pointer import  VOTablePointer
from utils.dict_utils import DictUtils
from client.objectbuilder.row_filter import RowFilter
from client.objectbuilder import row_filter
from astropy.table._column_mixins import sys
from client.objectbuilder.json_block_extractor import JsonBlockExtractor


class TemplatesIterator(object):
    '''
    classdocs
    '''


    def __init__(self, tableref, json_block, row_filter=None):
        '''
        Constructor
        '''
        self._xml_block = json_block        
        self._column_mapping = None
        self._table_iterator = None
        self._joined_templates = {}
        self._row_filter = row_filter
        self.tableref = tableref
        self.last_row = None
        logger.info("Create iterator on templates %s", self.tableref)
 
    def _map_columns(self):
        self._column_mapping = ColumnMapping(self._xml_block)
        self._column_mapping._map_columns()
        self._table_iterator = TableIterator(
            "iterator_key",
            VOTablePointer.get_table(self._column_mapping.table_name).to_table(),
            self._xml_block,
            self._column_mapping,
            row_filter=self._row_filter,
        )

    def _setup_joins(self):
        """
        """
        self._look_for_join(self._xml_block)
        
    def _look_for_join(self, array_element):
        if isinstance(array_element, list):

            if JsonTools.is_join(array_element) is True:
                # should never pass here 
                # TODO to be checked
                self._add_join(array_element, "arraY")
        elif isinstance(array_element, dict):
            for k, v in array_element.items():
                if isinstance(v, list) :
                    if JsonTools.is_join(v) is True:
                        print("k " + k)
                        self._add_join(v, k)

                elif isinstance(v, dict): 
                    self._look_for_join(v)
                    
    def _add_join(self, json_block, collection_role):
        join_block = {}
        foreign_column_id = None
        primary_column_id = None
        for k, v in json_block[0].items():
            if k == Ele.JOIN:
                tableref = v[Att.tableref]
                foreign_column_id = v[Ele.WHERE][Att.foreignkey]
                primary_column_id = v[Ele.WHERE][Att.primarykey]
            else:
                join_block[k] = v.copy()
        join_block[Att.tableref] = tableref
        row_filter = RowFilter(Att.tableref)
        templates_iterator = TemplatesIterator(tableref, join_block, row_filter=row_filter)
        templates_iterator._map_columns()
        row_filter.set_filtered_column_number(templates_iterator._column_mapping.get_col_index_by_name(foreign_column_id))
        row_filter.set_filtering_column_number(self._column_mapping.get_col_index_by_name(primary_column_id))
        #self._joined_templates[tableref] = templates_iterator
        self._joined_templates[collection_role] = templates_iterator
        logger.info("Iterator on joined table %s with role %s added", tableref, collection_role)

            
            
    def rewind(self):
        self._table_iterator._rewind()
        for _, v in self._joined_templates.items():
            v.rewind()

        
    def get_next_row(self):
        return self._table_iterator._get_next_row()
    
    def get_associated_data(self):
        row = self.last_row
        retour = {}
        if row is None:          
            return None
        
        for k, v in self._joined_templates.items():
            retour[k] = []

            v._table_iterator.row_filter.set_filtering_value(row[v._table_iterator.row_filter.filtering_column_number])
            v.rewind()

            while True:
                joined_row = v.get_next_flatten_row()
                if joined_row != None:
                    retour[k].append(joined_row)
                else :
                    break;

        return retour
        
    def get_next_flatten_row(self):
        self.last_row = self._table_iterator._get_next_flatten_row()
        return self.last_row
    
    def get_next_row_instance(self):
        retour =  self._table_iterator._get_next_row_instance()
        if retour is None:
            return None 
        self.last_row = retour["row"]
        instance = retour["instance"]
        for k, v in self._joined_templates.items():
            hook = JsonBlockExtractor.search_object_container(instance, k)[0]
            hook[k] = []
            v._table_iterator.row_filter.set_filtering_value(self.last_row[v._table_iterator.row_filter.filtering_column_number])
            v.rewind()

            while True:
                joined_row = v.get_next_row_instance()
                if joined_row != None:
                    hook[k].append(joined_row)
                else :
                    break;

        return instance
    
    def get_flatten_data_head(self):
        return self._table_iterator._get_flatten_data_head()