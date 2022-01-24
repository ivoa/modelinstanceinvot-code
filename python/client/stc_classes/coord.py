'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from .components import Quantity
from .coordsys import CoordSys

class Coord(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = None
        self.coordSys = None
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:Coordinate.coordSys"]'):
            self.coordSys = CoordSys.get_coordsys(ele)
        
    @staticmethod 
    def get_coord(model_view):
        dmtype = model_view.get("dmtype")
        
        if dmtype == "coords:PhysicalCoordinate":
            return PhysicalCoordinate(model_view)
        elif dmtype == "coords:LonLatPoint":
            return LonLatPoint(model_view)
        elif dmtype == "coords:ISOTime":
            return ISOTime(model_view)
        else:
            raise Exception(f"Point type {dmtype} not supported yet")
        

class PhysicalCoordinate(Coord):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.cval = None
        self.dmtype = "PhysicalCoordinate"

        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:PhysicalCoordinate.cval"]'):
            self.cval = Quantity(ele)
            break
 
    def __repr__(self):
        return f"[{self.dmtype}: {self.cval} {self.coordSys}]"
    
class TimeStamp(Coord):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        pass
 
    def __repr__(self):
        return f"[{self.dmtype}: {self.cval} {self.coordSys}]"
    
class ISOTime(Coord):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.datetime = None
        self.dmtype = "ISOTime"
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:ISOTime.date"]'):
            self.datetime = ele.get("value")
            break
        
    def __repr__(self):
        return f"[{self.dmtype}: {self.datetime} {self.coordSys}]"
        
class Point(Coord):
    '''
    classdocs
    '''


    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        pass
    
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

    def __repr__(self):
        if self.dist == None:
            return f"[{self.dmtype}: {self.lon} {self.lat} {self.coordSys}]"
        else:
            return f"[{self.dmtype}: {self.lon} {self.lat} {self.dist} {self.coordSys}]"

        