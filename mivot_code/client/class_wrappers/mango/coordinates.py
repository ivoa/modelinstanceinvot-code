'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..component_builder import ComponentBuilder
        
class UnitlessCoordinate(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.cval = None
        self.dmtype = "UnitlessCoordinate"
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="mango:stcextend.UnitlessCoord.frame"]'):
            self.frame = ComponentBuilder.get_coordframe(ele)

        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="mango:stcextend.UnitlessCoord.cval"]'):
            self.cval = ele.get("value")
            break
        self.label = f"[{self.cval} {self.frame.label}]"
        
    def __repr__(self):
        return self.label
