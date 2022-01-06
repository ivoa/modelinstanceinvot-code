'''
Created on 11 Dec 2021

@author: laurentmichel
'''

class MappingException(Exception):
    '''
    classdocs
    '''

    def __init__(self, message):
        '''
        Constructor
        '''
        self.message = message
    
    def __str__(self):
        return self.message