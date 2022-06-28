'''
Created on 7 juin 2022

@author: michel
'''
from ..component_builder import ComponentBuilder

from ..stc_classes.measure import Position, ProperMotion, Velocity
from .measures import Color, Photometry

class MangoObject(object):
        
    def __init__(self, model_view):
        """
         <INSTANCE dmrole="root" dmtype="mango:MangoObject">....
        """
        self._model_view = model_view
        self.identifier = None
        for ele in model_view.xpath("./ATTRIBUTE[@dmrole='mango:MangoObject.identifier']"):
            self.identifier = ele.get("value")
        self._parameters = []
        for ele in self._model_view.xpath("./COLLECTION/INSTANCE[@dmtype='mango:Parameter']"):
            self._parameters.append(MangoParameter(ele))

    
    def get_parameter_by_ucd(self, ucd_word):
        
        for param in self._parameters:
            if param.measure.ucd.startswith(ucd_word):
                return param
        return None

    def get_parameter_by_semantic(self, semantic_word):
        pass
    
    def get_parameter_by_description(self, description_word):
        pass
    

class MangoParameter(object):

    def __init__(self, model_view):
        """
         <INSTANCE dmrole="root" dmtype="mango:MangoObject">....
        """
        self._model_view = model_view
        self.semantic = None
        self.ucd = None
        self.description = None
        self.measure = None
        for ele in model_view.xpath("./ATTRIBUTE[@dmrole='mango:Parameter.semantic']"):
            self.semantic = ele.get("value")
        for ele in model_view.xpath("./ATTRIBUTE[@dmrole='mango:Parameter.ucd']"):
            self.ucd = ele.get("value")
        for ele in model_view.xpath("./ATTRIBUTE[@dmrole='mango:Parameter.description']"):
            self.description = ele.get("value")
        for ele in model_view.xpath("./INSTANCE[@dmrole='mango:Parameter.measure']"):
            self.measure = ComponentBuilder.get_measure(ele)
        
        self.label = f"{self.semantic} ({self.description}) {self.measure.label}"
     
    def __repr__(self):
        return self.label
 
    def isPosition(self):
        return isinstance(self.measure, Position) 
    
    def isProperMotion(self):
        return isinstance(self.measure, ProperMotion) 
    
    def isVelocity(self):
        return isinstance(self.measure, Velocity) 
    
    def isPhotometry(self):
        return isinstance(self.measure, Photometry) 
    
    def isColor(self):
        return (self.measure.ucd == "phot.flux;arith.ratio") 
   
    def get_associated_measures(self):
        pass
    


