'''
Created on Jan 15, 2021

Utility generating virtual collection replacing the GROUPBY block

@author: laurentmichel
'''
from copy import deepcopy
from client.inst_builder import logger
from utils.dict_utils import DictUtils


class GroupByProcessor(object):
    '''
    classdocs
    '''
    
    def __init__(self, table_name, gouping_col, table_template, data_table):
        '''
        :param table_template: JSON maping block of one table 
            ['MODEL_INSTANCE']['TABLE_MAPPING'][table_name]
        :param data_table: VOTABLE data table
        '''
        self.table_name = table_name
        self.gouping_col = gouping_col
        self.table_template = table_template
        self.data_table = data_table
        self.group_keys = set()
        
    def build_group_mapping(self):
        """
        Return a dict with the group values as keys and the the virtual collections as values
        """
        self.content_role = self._get_content_role()
        self._get_group_keys()
        ungrouped_mapping_block = {}
        
        for group_key in self.group_keys:
            # str conversion because Numpy values are not JSON serializable 
            ungrouped_mapping_block[str(group_key)] = self._get_group_mapping(group_key) 
            
        return ungrouped_mapping_block
    
    def _get_content_role(self):
        """
        Returns the role of the bock (instance) enclosed in the GROUPBY
        This role is the key which value is the instance. It is supposed not to
        start with a @. 
        """
        for  key in self.table_template["GROUPBY"].keys():
            if key.startswith("@") is False:
                return key
            
    def _get_group_keys(self):
        """
        Get from the table all different values of the group key 
        and store them in self.group_keys
        """
        gbkey = self.table_template["GROUPBY"]["@ref"]
        logger.info("GROUPBY (by %s) detected in table %s", gbkey, self.table_name)
        rowiter = iter(self.data_table)
        self.group_keys = set()
        for row in rowiter:
            self.group_keys.add(row[gbkey])

    def _get_group_mapping(self, group_key):
        """
        Build a virtual collection for a particular group key
        The role of the instance enclosed in the collection is the concatenation of
        the original role with the group key
        The group key is used as filter value each collection
        It converted in str because Numpy values are not JSON serialisable
        The filter is propagated to the enclosed TABLE_ROW_TEMPLATE
        TODO only the 1st TABLE_ROW_TEMPLATE because DictUtils.find_item_by_key returns after one match
        """
        row_filter = {
            "@ref": self.gouping_col,
            "@value": str(group_key)
            }
        retour = { 
                    "TABLE_ROW_TEMPLATE": {
                        "FILTER": row_filter,
                        (self.content_role + "_" + str(group_key)): deepcopy(
                            self.table_template["GROUPBY"][self.content_role]
                            )
                    }
                }            
        trws = DictUtils.find_item_by_key(retour["TABLE_ROW_TEMPLATE"], "TABLE_ROW_TEMPLATE")
        for trw in trws:
            trw["FILTER"] = row_filter
        return [ retour ]
        
