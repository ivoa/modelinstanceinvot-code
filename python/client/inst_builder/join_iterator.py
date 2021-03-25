'''
Created on 30 juin 2020

@author: laurentmichel
'''
from client.inst_builder.table_iterator import TableIterator
from client.inst_builder.row_filter import RowFilter
from utils.dict_utils import DictUtils
from client import logger


class JoinIterator(object):
    '''
    classdocs
    '''

    def __init__(self,
                 foreign_table,
                 primary_key,
                 foreign_key,
                 json_join_content):
        self.foreign_table = foreign_table
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.json_join_content = json_join_content
        self.table_mapper = None
        self.parsed_table = None
        self.row_filter = None
        # print(DictUtils.get_pretty_json(self.json_join_content))
        
    def __repr__(self):
        return "Join iterator f_table={} p_key={}, f_key={}".format(
            self.foreign_table, self.primary_key, self.foreign_key)
        
    def connect_votable(self, parsed_table):
        from client.inst_builder.table_mapper import TableMapper
        self.parsed_table = parsed_table
        ack = None
        acv = None
        for k in self.json_join_content.keys():
            if k.startswith("@") is False:
                ack = k
                acv = self.json_join_content[k]
                break
        logger.info("Build table_mapper for data joint with table %s", self.foreign_table)
        self.table_mapper = TableMapper(
            self.foreign_table,
            None,
            parsed_table=self.parsed_table,
            json_inst_dict={
                "MODEL_INSTANCE": {
                    "@name": "MANGO",
                    "@syntax": "ModelInstInVot",
                   # "MODELS":{},
                    "GLOBALS":{},
                    "TABLE_MAPPING": {
                        self.foreign_table: {
                            "@tableref": self.foreign_table,
                            "root": [
                                    {
                                    "TABLE_ROW_TEMPLATE": {
                                        "FILTER": {
                                            "@ref": self.foreign_key,
                                            "@value":-1
                                            },
                                        ack: acv
                                        },
                                    }
                                ]
                            }
                        }
                    }
                }
            )
        self.table_mapper.resolve_refs_and_values(resolve_dmrefs=False)
        self.table_mapper.map_columns()
        for _, table_iterator in self.table_mapper.table_iterators.items():
            self.row_filter = table_iterator.row_filter
            break;

    def set_foreignkey_value(self, value):   
        self.row_filter.value = value
        self.table_mapper.rewind()
        
    def get_subset_instance(self, key_value):
        self.row_filter = RowFilter({
                "@ref": self.foreign_key,
                "@value": key_value
                })
        self.table_iterator = TableIterator(
                                "join",
                                self.table_votable,
                                self.json_join_content,
                                self.column_mapping,
                                self.row_filter
                                )
    
