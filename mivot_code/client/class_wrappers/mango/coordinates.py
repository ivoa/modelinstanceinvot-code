'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..stc_classes.coord import Coord

        
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
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="mango:stcextend.UnitlessCoord.cval"]'):
            self.cval = ele.get("value")
            break
        self.label = f"[{self.cval} {self.coordSys.label}]"
        
    def __repr__(self):
        return self.label
