'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from ..component_builder import ComponentBuilder
from ..root_class import RootClass
from .components import Quantity
from mivot_code.utils.xml_utils import XmlUtils

class Coord(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = None
        self.coordSys = None
        self._set_coord_sys(model_view)
        
        if self.coordSys is not None:
            self.label = f"{self.__class__} {self.coordSys.label}"
        else:
            self.label = f"{self.__class__}"
       
    def _set_coord_sys(self, model_view): 
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:Coordinate.coordSys"]'):
            self.coordSys = ComponentBuilder.get_coordsys(ele)
            return

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
        if self.cval is None:
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:PhysicalCoordinate.cval"]'):
                self.cval = Quantity(ele)
                break
       
        if self.coordSys is not None:
            self.label = f"[{self.cval.value} {self.cval.unit} {self.coordSys.label}]"
        else:            
            self.label = f"[{self.cval.value} {self.cval.unit}]"


    def __repr__(self):
        return self.label

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
        return self.label
    
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
        return self.label
        
class MJD(Coord):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.date = None
        self.dmtype = "MJD"
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:MJD.date"]'):
            self.date = float(ele.get("value"))
            break
        
        if self.coordSys is not None:
            self.label = f"[{self.date}d {self.coordSys.label}]"
        else:            
            self.label = f"[{self.date}d]"
        
    def __repr__(self):
        return self.label
        
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
        if self.lon is None:
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:LonLatPoint.lon"]'):
                self.lon = Quantity(ele)

        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:LonLatPoint.lat"]'):
            self.lat = Quantity(ele)
        if self.lat is None:
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:LonLatPoint.lat"]'):
                self.lat = Quantity(ele)
            
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:LonLatPoint.dist"]'):
            self.dist = Quantity(ele)
        if self.dist is None:
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="coords:LonLatPoint.dist"]'):
                self.dist = Quantity(ele)

        self.label = "["
        if self.lon is not None:
            self.label += f"{self.lon.label}"
        if self.lat is not None:
            self.label += f" {self.lat.label}"
        if self.dist is not None:
            self.label += f" {self.dist.label}"
        if self.coordSys is not None:
            self.label += f" {self.coordSys.label}"
        self.label += "]"
        
        