'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from .error import Error
from .coord import Coord
from mivot_code.utils.xml_utils import XmlUtils

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
        
        for ele in model_view.xpath("./ATTRIBUTE[@dmrole='mango:Parameter.ucd']"):
            self.ucd = ele.get("value")
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Measure.error"]'):
            for subele in ele.xpath('.//INSTANCE[@dmrole="meas:Error.statError"]'):
                self.error = Error.get_error(subele)
                break
            
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="meas:Measure.ucd"]'):
            self.ucd = ele.get("value")
            break

        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Measure.coord"]'):
            print("================>>>>>")
            self.coord = Coord.get_coord(ele)
            break

    @staticmethod 
    def get_measure(model_view):
        """
        Returns the Measure instance matching model_view
        """
        
        dmtype = model_view.get("dmtype")
        if dmtype == "meas:Position":
            return Position(model_view)
        elif dmtype == "meas:Time":
            return Time(model_view)
        elif dmtype == "meas:Velocity":
            return Velocity(model_view)
        elif dmtype == "meas:GenericMeasure":
            return GenericMeasure(model_view)
        else:
            # for now mango measures are taken as generic measures
            return GenericMeasure(model_view)

            #else:
            #    raise Exception(f'Measure {dmtype} not supported yet')
            
        raise Exception('This element is not a Measure')

    def __repr__(self):
        return f"ucd: {self.ucd} coords: {self.coord} error: {self.error}"
    
        
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
        return f"ucd: {self.ucd} coords: {self.coord} error: {self.error}"
    
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
        return f"ucd: {self.ucd} coords: {self.coord} error: {self.error}"
    
        
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
        return f"ucd: {self.ucd} coords: {self.coord} error: {self.error}"

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
        return f"ucd: {self.ucd} coords: {self.coord} error: {self.error}"
    


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
        return f"ucd: {self.ucd} coslat:{self.cosLat_applied} coords: {self.coord} error: {self.error}"

