'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from ..component_builder import ComponentBuilder
from .components import Quantity
from .coordsys import CoordSys


class Point(object):
    '''
    classdocs
    '''


    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.coordSys = None
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:Coordinate.coordSys"]'):
            self.coordSys = ComponentBuilder.get_coordsys(ele)
        
    @staticmethod 
    def get_point(model_view):
        dmtype = model_view.get("dmtype")
        if dmtype == "coords:LonLatPoint":
            return LonLatPoint(model_view)
        else:
            raise Exception(f"Point type {dmtype} not supported yet")
    
class LonLatPoint(Point):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.lon = None
        self.lat = None
        self.dist = None
        self.dmtype = "LonLatPoint"
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:LonLatPoint.lon"]'):
            self.lon = Quantity(ele)
            break
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:LonLatPoint.lat"]'):
            self.lat = Quantity(ele)
            break
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:LonLatPoint.dist"]'):
            self.dist = Quantity(ele)
            break
        self.label = f"[{self.dmtype}: {self.lon} {self.lat} {self.coordSys}]"

    def __repr__(self):
        return self.label
        