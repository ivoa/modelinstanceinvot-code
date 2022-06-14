'''
Created on 7 juin 2022

@author: michel
'''
from client.stc_classes.measure import Measure

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
            print("add")
            self._parameters.append(MangoParameter(ele))

    
    def get_parameter_by_ucd(self, ucd_word):
        
        for param in self._parameters:
            if param.ucd.startswith(ucd_word):
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
        for ele in model_view.xpath("./ATTRIBUTE[@dmrole='mango:Parameter.semantic']"):
            self.description = ele.get("value")
        self.measure = Measure.get_measure(model_view)
    
    def get_associated_measures(self):
        pass

