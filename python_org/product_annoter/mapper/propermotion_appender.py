'''
Created on 15 avr. 2020

@author: laurentmichel
'''
import os
from product_annoter.mapper import logger
from product_annoter.mapper.constants import PARAM_TABLE_MAPPING
from product_annoter.mapper.parameter_appender import ParameterAppender


class ProperMotionAppender:
    '''
    classdocs
    '''
    
    def __init__(self, output_mapping_path, component_path):           
        '''
        Constructor
        :param output_mapping_path: Output file with just the mapping block
        :type output_mapping_path: string
        :param component_path: Directory with all the mapping components
        :type component_path: string
        '''
        self.output_mapping_path = output_mapping_path    
        self.component_path = component_path  
        # get the mapping component attached to this appender
        self.position_path = os.path.join(component_path,
                                          "mango.ProperMotion.mapping.xml")
        logger.info("read  component %s", self.position_path)

        # Build the appender instance
        # The appender is in charge of all operations modifying the mapping component
        # to build an XML block ready to be inserted to the mapping
        self.appender = ParameterAppender(
            PARAM_TABLE_MAPPING.POSITION,
            self.output_mapping_path,
            self.position_path
            )
    
    def append_measure(self, json_measure_descriptor):  
        """
        push the values and refs read in the config into the new mapping block
        :param json_measure_descriptor: description of the position measure
        :type json_measure_descriptor: dict
        """
        self.set_param_semantic(json_measure_descriptor["ucd"],
                                json_measure_descriptor["semantic"],
                                json_measure_descriptor["description"],
                                json_measure_descriptor["reductionStatus"]
                                )
        
        self.set_position(json_measure_descriptor["position"]["longitude"],
                          json_measure_descriptor["position"]["latitude"],
                          json_measure_descriptor["position"]["unit"]
                          ) 
        self.set_errors(json_measure_descriptor["errors"]["random"]["longitude"],
                        json_measure_descriptor["errors"]["random"]["latitude"],
                        json_measure_descriptor["errors"]["random"]["unit"])
            
        self.set_notset_value()
        self.appender.insert_parameter_block()
             
    def set_position(self, ra_ref, dec_ref, unit):
        self.appender.set_ref_or_value("meas:ProperMotion.lon",
                               "ivoa:RealQuantity.value",
                               ra_ref)
        self.appender.set_ref_or_value("meas:ProperMotion.lon",
                               "ivoa:Quantity.unit",
                               unit)
        self.appender.set_ref_or_value("meas:ProperMotion.lat",
                               "ivoa:RealQuantity.value",
                               dec_ref)
        self.appender.set_ref_or_value("meas:ProperMotion.lat",
                               "ivoa:Quantity.unit",
                               unit)
                                     
    def set_errors(self,
                   err_ref_ra, err_ref_dec , err_unit):
        
        self.appender.set_ref_or_value("meas:Ellipse.posAngle",
                                    "ivoa:RealQuantity.value",
                                    "0.0")
        self.appender.set_ref_or_value("meas:Ellipse.posAngle",
                                    "ivoa:Quantity.unit",
                                    "deg")

        if err_ref_ra is not None:
            
            self.appender.set_ref_or_value("meas:Ellipse.semiAxis",
                                  "ivoa:RealQuantity.value",
                                  err_ref_ra, rank=0)
        
            self.appender.set_ref_or_value("meas:Ellipse.semiAxis",
                                    "ivoa:RealQuantity.value",
                                    err_ref_dec, rank=1)
            self.appender.set_ref_or_value("meas:Ellipse.semiAxis",
                                    "ivoa:Quantity.unit",
                                    err_unit)
             
    def set_param_semantic(self, ucd, semantic, description, reduction_status):
        self.appender.set_param_semantic(ucd, semantic, description, reduction_status) 

    def set_notset_value(self):
        self.appender.set_notset_value()
        
    def tostring(self):
        return self.appender.tostring()
        
    def save(self, output_path):
        """
        Just for the developper to have a snapshot
        """
        self.appender.save(output_path)
        
