'''
Created on 7 juin 2022

@author: michel
'''
from ..stc_classes.measure import Measure

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
            self.measure = Measure.get_measure(ele)
     
    def __repr__(self):
        return f"{self.semantic} : {self.description}"
 
    def get_associated_measures(self):
        pass
    
    @staticmethod 
    def get_measure(model_view):
        """
        Returns the Measure instance matching model_view
        """
        
        dmtype = model_view.get("dmtype")
        if dmtype == "mango:stcextend.HardnessRatio":
            return HardnessRatio(model_view)
        elif dmtype == "mango:stcextend.Photometry":
            return Photometry(model_view)
        else:
            # for now mango measures are taken as generic measures
            return Measure.get_measure(model_view)(model_view)

            #else:
            #    raise Exception(f'Measure {dmtype} not supported yet')
            
        raise Exception('This element is not a Measure')

class HardnessRatio(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)

    def __repr__(self):
        return f"ucd: {self.ucd} coords: {self.coord} error: {self.error}"


class Photometry(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)

    def __repr__(self):
        return f"ucd: {self.ucd} coords: {self.coord} error: {self.error}"
