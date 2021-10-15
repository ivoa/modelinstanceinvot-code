"""
Created on 30 juin 2020

@author: laurentmichel
"""
from client.objectbuilder.table_iterator import TableIterator

from client.objectbuilder.row_filter import RowFilter
from client import logger
from client.translator.vocabulary import Ele, Att


class JoinIterator(object):
    """
    classdocs
    """
    
    def __init__(self, json_join_content):
        self.foreign_table = json_join_content[Ele.JOIN][Att.tableref]
        self.foreign_key = json_join_content[Ele.JOIN][Ele.WHERE][Att.foreignkey]
        self.primary_key = json_join_content[Ele.JOIN][Ele.WHERE][Att.primarykey]
        self.json_join_content = json_join_content
        self.table_mapper = None
        self.parsed_table = None
        self.row_filter = None

    def __repr__(self):
        return "Join iterator f_table={} p_key={}, f_key={}".format(
            self.foreign_table, self.primary_key, self.foreign_key
        )

    def connect_votable(self, parsed_table):
        from client.objectbuilder.table_mapper import TableMapper

        self.parsed_table = parsed_table
        ack = None
        acv = None
        for key, value in self.json_join_content.items():
            if key.startswith("@") is False and key != Ele.JOIN:
                ack = key
                acv = value
                break
        logger.info(
            "Build table_mapper for data joint with table %s", self.foreign_table
        )
        self.table_mapper = TableMapper(
            self.foreign_table,
            None,
            parsed_table=self.parsed_table,
            json_inst_dict={
                "dm-mapping:VODML": {
                    # "MODELS":{},
                    "dm-mapping:GLOBALS": {},
                    "dm-mapping:TEMPLATES": {
                        self.foreign_table: {
                            "@tableref": self.foreign_table,
                            "dm-mapping:WHERE": {
                                "@primarykey": self.foreign_key,
                                "@value": -1,
                            },
                            "root": {ack: acv},
                        }
                    },
                }
            },
        )
        self.table_mapper.resolve_refs_and_values(resolve_dmrefs=False)
        self.table_mapper.map_columns()
        for _, table_iterator in self.table_mapper.table_iterators.items():
            self.row_filter = table_iterator.row_filter
            break

    def set_foreignkey_value(self, value):
        self.row_filter.value = value
        self.table_mapper.rewind()

    def get_subset_instance(self, key_value):
        self.row_filter = RowFilter({"@ref": self.foreign_key, "@value": key_value})
        self.table_iterator = TableIterator(
            "join",
            self.table_votable,
            self.json_join_content,
            self.column_mapping,
            self.row_filter,
        )
