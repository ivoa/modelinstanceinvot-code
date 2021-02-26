'''
Created on 15 avr. 2020

@author: laurentmichel
'''

from product_annoter.mapper.constants import PARAM_TABLE_MAPPING
from product_annoter.mapper.parameter_appender import ParameterAppender


class IdentifierAppender:
    '''
    classdocs
    '''
    
    def __init__(self, mango_path):
        '''
        Constructor
        '''
        self.mango_path = mango_path        
        
        self.appender = ParameterAppender(
            PARAM_TABLE_MAPPING.POSITION,
            self.mango_path,
            ""
            )

        self.appender.add_globals()
        self.appender.insert_parameter_block()
    
    def append_measure(self, source_descriptor):  
        self.set_identifier(source_descriptor["identifier"])

        self.set_notset_value()

    def set_identifier(self, identifier_ref):
        self.appender.set_ref("root",
                              "mango:MangoObject.identifier",
                              identifier_ref)

    def set_notset_value(self):
        self.appender.set_notset_value()
        
    def tostring(self):
        return self.appender.tostring()
        
    def save(self, output_path):
        self.appender.save(output_path)
        
