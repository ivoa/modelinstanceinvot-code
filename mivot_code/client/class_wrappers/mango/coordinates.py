'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..stc_classes.coordinates import Coord
from ..component_builder import ComponentBuilder
from mivot_code.utils.xml_utils import XmlUtils
        
class UnitlessCoordinate(Coord):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.cval = None
        self.dmtype = "UnitlessCoordinate"
        self.frame = ComponentBuilder.get_coordframe(
            XmlUtils.get_instance_by_role(model_view,
                                          "mango:stcextend.UnitlessCoord.frame"))
        self.cval = XmlUtils.get_attribute_value_by_role(model_view, "mango:stcextend.UnitlessCoord.cval")
        self.label = f"[{self.cval} {self.frame.label}]"
        

class FlagCoord(Coord):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.cval = None
        self.dmtype = "FlagCoord"
        
        self.frame = ComponentBuilder.get_coordframe(
            XmlUtils.get_instance_by_role(model_view,
                                          "mango:stcextend.Flag.dictionary"))
        self.cval = XmlUtils.get_attribute_value_by_role(model_view, "mango:stcextend.FlagCoord.coord")
        self.label = f"[{self.cval} {self.frame.get_label(self.cval)}]"
        
