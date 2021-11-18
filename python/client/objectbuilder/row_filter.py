'''
Created on 1 avr. 2020

@author: laurentmichel
'''

class RowFilter(object):
    '''
    Class holder for the parameter needed to filter row
    '''

    def __init__(self, name):
        '''
        '''

        self.name = name
 
        self.filtered_column_number = None
        self.filtering_value = None
        self.filtering_column_number = None
     
    def __repr__(self):
        """
        """
        return "RowFilter {} filtered_column_number={}  filtering_column_number={} filtering_value={}".format(
            self.name, self.filtered_column_number, self.filtering_column_number, self.filtering_value)
    
    def set_filtered_column_number(self, filtered_column_number):
        self.filtered_column_number = filtered_column_number
        
    def set_filtering_column_number(self, filtering_column_number):
        self.filtering_column_number = filtering_column_number
        
    def set_filtering_value(self, filtering_value):
        self.filtering_value = filtering_value
        
    
    def row_match(self, row):
        """
        :param row: data row
        :type row: numpy table row
        :return: true if the data row matches the filtering condition
        :rtype: boolean
        """
        if self.filtered_column_number is None or self.filtering_value is None:
            return True
        if str(row[self.filtered_column_number]) == str(self.filtering_value):
            return True
        return False
