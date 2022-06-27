'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from ..component_builder import ComponentBuilder
from .error import Error

class Measure(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.coord = None
        self.error = None
        self.ucd = None
        
        self._set_ucd(model_view)
        self._set_error(model_view)
        self._set_coord(model_view)
        
        self.label = f"{self.ucd}={self.coord.label}"
 
        
    def _set_ucd(self, model_view):
        for ele in model_view.xpath("./ATTRIBUTE[@dmrole='mango:Parameter.ucd']"):
            self.ucd = ele.get("value")
    
    def _set_error(self, model_view):
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Measure.error"]'):
            for subele in ele.xpath('.//INSTANCE[@dmrole="meas:Error.statError"]'):
                self.error = ComponentBuilder.get_error(subele)
                break

    def _set_coord(self, model_view):
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Measure.coord"]'):
            self.coord = ComponentBuilder.get_coord(ele)
            break
      

    def __repr__(self):
        return self.label
    
        
class GenericMeasure(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)

    def __repr__(self):
        return self.label

    
class Time(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.error = None

    def __repr__(self):
        return self.label
    
        
class Position(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)

    def __repr__(self):
        return self.label

class Velocity(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)

    def __repr__(self):
        return self.label
    


class ProperMotion(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.cosLat_applied = "True"
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="meas:ProperMotion.cosLat_applied"]'):
            self.cosLat_applied = ele.get("value")
            break


    def __repr__(self):
        return self.label

