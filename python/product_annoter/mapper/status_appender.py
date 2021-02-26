'''
Created on 15 avr. 2020

@author: laurentmichel
'''

from product_annoter.mapper.constants import PARAM_TABLE_MAPPING
from product_annoter.mapper.parameter_appender import ParameterAppender


class StatusAppender:
    '''
    classdocs
    '''
    
    def __init__(self, mango_path, param_path):
        '''
        Constructor
        '''
        self.mango_path = mango_path        
        self.status_path = param_path
        
        self.appender = ParameterAppender(
            PARAM_TABLE_MAPPING.POSITION,
            self.mango_path,
            self.status_path
            )

        self.appender.add_globals()
        self.appender.add_param_parameter()
    
    def append_measure(self, measure_descriptor):  
        self.set_param_semantic(measure_descriptor["ucd"],
                                measure_descriptor["semantic"],
                                measure_descriptor["description"]
                                )
        
        self.set_identifier(measure_descriptor["identifier"])

        self.set_status(measure_descriptor["status"]["value"]) 
        self.set_notset_value()
        
    def set_spaceframe(self, frame, equinox):   
        
        self.appender.set_value("coords:PhysicalCoordSys.frame" ,
                                "coords:SpaceFrame.spaceRefFrame",
                                frame);
        if equinox is not None:
            self.appender.set_value(
                "coords:PhysicalCoordSys.frame" ,
                "coords:SpaceFrame.equinox",
                equinox);
    
    def set_status(self, status_ref):
        self.appender.set_ref("mango:STCStatus.coord",
                              "mango:STCStatusState.status",
                              status_ref)
            
    def set_param_semantic(self, ucd, semantic, description):
        self.appender.set_param_semantic(ucd, semantic, description) 

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
        
