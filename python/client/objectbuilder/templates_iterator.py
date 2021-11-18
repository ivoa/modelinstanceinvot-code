'''
Created on 18 Nov 2021

@author: laurentmichel
'''
from utils.json_tools import JsonTools
from client.translator.vocabulary import Att, Ele
from client.objectbuilder.column_mapping import ColumnMapping
from client.objectbuilder.table_iterator import TableIterator
from client.objectbuilder.votable_pointer import  VOTablePointer
from utils.dict_utils import DictUtils
from client.objectbuilder.row_filter import RowFilter
from client.objectbuilder import row_filter
from astropy.table._column_mixins import sys


class TemplatesIterator(object):
    '''
    classdocs
    '''


    def __init__(self, json_block, row_filter=None):
        '''
        Constructor
        '''
        self._json_block = json_block        
        self._column_mapping = None
        self._table_iterator = None
        self._joined_templates = {}
        self._row_filter = row_filter
        
    def _map_columns(self):
        self._column_mapping = ColumnMapping(self._json_block)
        self._column_mapping._map_columns()
        self._table_iterator = TableIterator(
            "iterator_key",
            VOTablePointer.get_table(self._column_mapping.table_name).to_table(),
            self._json_block,
            self._column_mapping,
            row_filter=self._row_filter,
        )

    def _setup_joins(self):
        """
        """
        self._look_for_join(self._json_block)
        
    def _look_for_join(self, array_element):
        if isinstance(array_element, list):

            if JsonTools.is_join(array_element) is True:
                self._add_join(array_element)
        elif isinstance(array_element, dict):
            for _, v in array_element.items():
                if isinstance(v, list) :
                    if JsonTools.is_join(v) is True:
                        self._add_join(v)

                elif isinstance(v, dict): 
                    self._look_for_join(v)
                    
    def _add_join(self, json_block):
        join_block = {}
        foreign_column_id = None
        primary_column_id = None
        for k, v in json_block[0].items():
            if k == Ele.JOIN:
                tableref = v[Att.tableref]
                DictUtils.print_pretty_json(v)
                foreign_column_id = v[Ele.WHERE][Att.foreignkey]
                primary_column_id = v[Ele.WHERE][Att.primarykey]
                print(">>>>>>>> " + foreign_column_id)
            else:
                join_block[k] = v.copy()
        join_block[Att.tableref] = tableref
        DictUtils.print_pretty_json(join_block)
        row_filter = RowFilter(Att.tableref)
        templates_iterator = TemplatesIterator(join_block, row_filter=row_filter)
        templates_iterator._map_columns()
        row_filter.set_filtered_column_number(templates_iterator._column_mapping.get_col_index_by_name(foreign_column_id))
        print("==============")
        print(foreign_column_id)
        print(templates_iterator._column_mapping)
        print(templates_iterator._column_mapping.get_col_index_by_name(foreign_column_id))
        import sys
        sys.exit(1)
        print(self._column_mapping.get_col_index_by_name(primary_column_id))
        row_filter.set_filtering_column_number(self._column_mapping.get_col_index_by_name(primary_column_id))
        
        print(row_filter)
        self._joined_templates[tableref] = templates_iterator
            
            
    def rewind(self):
        self._table_iterator._rewind()
        for _, v in self._joined_templates.items():
            v._rewind()

        
    def get_next_row(self):
        return self._table_iterator._get_next_row()
    
    def get_next_flatten_row(self):
        row = self._table_iterator._get_next_flatten_row()
        for k, v in self._joined_templates.items():

            v._table_iterator.row_filter.set_filtering_value(row[v._table_iterator.row_filter.filtering_column_number])
            v.rewind()
            print("<<<<<<<<<<<<<>>>>>>>>>>>> " + k)
            print(v._table_iterator.row_filter)
            while True:
                joined_row = v.get_next_flatten_row()
                if joined_row != None:
                    print(joined_row)
                else :
                    break;
        return row
    
    def get_next_row_instance(self):
        return self._table_iterator._get_next_row_instance()
    
    def get_flatten_data_head(self):
        return self._table_iterator._get_flatten_data_head()