'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from ..component_builder import ComponentBuilder
from ..root_class import RootClass
from mivot_code.utils.xml_utils import XmlUtils


class Measure(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.coord = None
        self.error = None
        self.ucd = None
        
        self._set_ucd(model_view)
        self._set_error(model_view)
        self._set_coord(model_view)

        if self.error is not None:
            self.label = f"{self.ucd}={self.coord.label} +/-{self.error.label}"
        else:
            self.label = f"{self.ucd}={self.coord.label} "

    def _set_ucd(self, model_view):
        self.ucd = XmlUtils.get_attribute_value_by_role(model_view, 'meas:Measure.ucd')
    
    def _set_error(self, model_view):
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Measure.error"]'):
            for subele in ele.xpath('.//INSTANCE[@dmrole="meas:Error.statError"]'):
                self.error = ComponentBuilder.get_error(subele)
                break

    def _set_coord(self, model_view):
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Measure.coord"]'):
            self.coord = ComponentBuilder.get_coord(ele)
            break    

    
class GenericMeasure(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.dmtype = "GenericMeasure"

    
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
        self.dmtype = "Time"
    
        
class Position(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.dmtype = "Position"

class Velocity(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.dmtype = "Velocity"


class ProperMotion(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.dmtype = "ProperMotion"
        self.cosLat_applied = "True"
        self.cosLat_applied = XmlUtils.get_attribute_value_by_role(
            model_view,
            "meas:ProperMotion.cosLat_applied")


