'''
Created on 1 avr. 2020

@author: laurentmichel
'''


class RowFilter(object):
    '''
    Class holder for the parameter needed to filter row
    '''

    def __init__(self, json_block):
        '''
        Constructor
        :param json_block: content of a "WHERE" key
        :type json_block: Dict
        '''
        if "@name" in json_block.keys():
            self.name = json_block["@name"]   
        else:
            self.name = "NoName"
            
        # Value be applied by the filter
        self.value = json_block["@value"]   
        # Reference of the FIELD to be used by the filter evaluator     
        self.key = json_block["@primarykey"]
        # The filtering is don on values located by their column number
        self.col_number = -1
     
    def __repr__(self):
        """
        """
        return "Row filter {} key={} value={} col={}".format(self.name, self.key, self.value, self.col_number)
        
    def map_col_number(self, column_mapping):
        """
        Set the number of the column to be used by the filter
        :param column_mapping: needed to bind self.key with column index
        :type column_mapping: ColumnMapping instance
        """
        self.col_number = column_mapping.get_col_index_by_name(self.key)
    
    def row_match(self, row):
        """
        :param row: data row
        :type row: numpy table row
        :return: true if the data row matches the filtering condition
        :rtype: boolean
        """
        if str(row[self.col_number]) == str(self.value):
            return True
        return False
