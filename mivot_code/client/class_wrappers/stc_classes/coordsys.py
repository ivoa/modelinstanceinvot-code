'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from .components import Quantity 
from pickle import NONE

class CoordSys(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = None
        self.label = f"{self.__class__}"

    
class TimeFrame(CoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = "TimeFrame"
        self.timescale = None
        self.reflocation = None
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:TimeFrame.timescale"]'):
            self.timescale = ele.get("value")
            break
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:StdRefLocation.position"]'):
            self.reflocation = ele.get("value")
            break
        self.label = f"[{self.timescale} {self.reflocation}]"
    
    def __repr__(self):
        return self.label
    
class SpaceFrame(CoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = None

    @staticmethod 
    def get_spaceframe(model_view):
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:SpaceFrame.spaceRefFrame"]'):
            if ele.get("value") == "ICRS":
                return ICRS(ele)
            elif ele.get("value") == "Galactic":
                return Galactic(ele)
            else:
                raise Exception(f'Coordsys {ele.get("value")} not supported yet')
        raise Exception('No coordsys found')
    
class ICRS(SpaceFrame):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = "ICRS"
        self.label = "ICRS"
        
    def __repr__(self):
        return self.label
    
class Galactic(SpaceFrame):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.label = "Galactic"
        
    def __repr__(self):
        return self.label