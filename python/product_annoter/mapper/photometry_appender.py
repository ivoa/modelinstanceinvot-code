'''
Created on 15 avr. 2020

@author: laurentmichel
'''
import os
from product_annoter.mapper.constants import PARAM_TABLE_MAPPING
from product_annoter.mapper.parameter_appender import ParameterAppender


class PhotometryAppender:
    '''
    classdocs
    '''
    
    def __init__(self, mango_path, component_path):           
        '''
        Constructor
        '''
        self.mango_path = mango_path    
        self.component_path = component_path  
        self.position_path = os.path.join(component_path,
                                          "mango.Photometry.mapping.xml")
        self.appender = ParameterAppender(
            PARAM_TABLE_MAPPING.POSITION,
            self.mango_path,
            self.position_path
            )

    def append_measure(self, measure_descriptor):  
        self.set_param_semantic(measure_descriptor["ucd"],
                                measure_descriptor["semantic"],
                                measure_descriptor["description"],
                                measure_descriptor["reductionStatus"]
                               )
        
        self.connect_spaceframe(measure_descriptor["frame"]["frame"])
        self.set_position(measure_descriptor["luminosity"]["luminosity"]
                          ) 
        
        self.set_errors(measure_descriptor["errors"]) 
        self.set_notset_value()
        self.appender.insert_parameter_block()
        self.set_spaceframe(measure_descriptor["frame"]["frame"])
        
    def connect_spaceframe(self, frame):   
        self.appender.set_dmref("coords:Coordinate.coordSys", "PhotFrame_" + frame)
        return
    
    def set_spaceframe(self, frame):   
        with open(os.path.join(self.component_path, "mango.frame." + frame + ".xml")) as xml_file:
            data = xml_file.read()
            self.appender.add_instance_to_globals(data)
        return
             
    def set_position(self, luminosity):
        self.appender.set_ref_or_value("mango:stcextend.Photometry.coord",
                              "mango:stcextend.PhotometryCoord.luminosity",
                              luminosity)
                                     
    def set_errors(self, error_object):
        
        if "random" in error_object.keys():
            rand = error_object["random"]
            if "value" in rand.keys() is not None:
                self.appender.set_ref_or_value("meas:Error.statError",
                    "ivoa:RealQuantity.value",
                     rand["value"])
            if "unit" in rand.keys() is not None:
                self.appender.set_ref_or_value("meas:Error.statError",
                    "ivoa:RealQuantity.unit",
                     rand["unit"])
            
    def set_param_semantic(self, ucd, semantic, description, reduction_status):
        self.appender.set_param_semantic(ucd, semantic, description, reduction_status) 

    def set_notset_value(self):
        self.appender.set_notset_value()
        
    def tostring(self):
        return self.appender.tostring()
        
    def save(self, output_path):
        self.appender.save(output_path)
        
