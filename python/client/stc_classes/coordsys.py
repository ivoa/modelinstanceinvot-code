'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from .components import Quantity 

class CoordSys(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
    
    @staticmethod 
    def get_coordsys(model_view):
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:SpaceFrame.spaceRefFrame"]'):
            if ele.get("value") == "ICRS":
                return ICRS(ele)
            elif ele.get("value") == "Galactic":
                return Galactic(ele)
            else:
                raise Exception(f'Coordsys {ele.get("value")} not supported yet')
        raise Exception('No coordsys found')
    
class ICRS(CoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = "ICRS"
        
    def __repr__(self):
        return f"{self.dmtype}"
    
class Galactic(CoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = "Galactic"
        
    def __repr__(self):
        return f"{self.dmtype}"