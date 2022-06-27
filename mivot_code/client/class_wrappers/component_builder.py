'''
Created on 27 Jun 2022

@author: laurentmichel
'''

class ComponentBuilder(object):
    '''
    classdocs
    '''

    @staticmethod
    def get_measure(model_view):
        """
        Returns the Measure instance matching model_view
        """
        from .stc_classes.measure import Position, Time, Velocity, GenericMeasure
        from .mango.measures import Color, Photometry
        
        dmtype = model_view.get("dmtype")
        if dmtype == "meas:Position":
            return Position(model_view)
        elif dmtype == "meas:Time":
            return Time(model_view)
        elif dmtype == "meas:Velocity":
            return Velocity(model_view)
        elif dmtype == "meas:GenericMeasure":
            return GenericMeasure(model_view)
        elif dmtype == "mango:stcextend.Color":
            return Color(model_view)
        elif dmtype == "mango:stcextend.Photometry":
            return Photometry(model_view)
        else:
            raise Exception(f"Measure type {dmtype} not supported yet")

    @staticmethod 
    def get_coord(model_view):
        from .stc_classes.coord import PhysicalCoordinate, LonLatPoint, ISOTime
        from .mango.coordinates import UnitlessCoordinate
        dmtype = model_view.get("dmtype")
        
        if dmtype == "coords:PhysicalCoordinate":
            return PhysicalCoordinate(model_view)
        elif dmtype == "coords:LonLatPoint":
            return LonLatPoint(model_view)
        elif dmtype == "coords:ISOTime":
            return ISOTime(model_view)
        elif dmtype == "mango:stcextend.UnitlessCoordinate":
            return UnitlessCoordinate(model_view)
        else:
            raise Exception(f"Coordinate type {dmtype} not supported yet")

    @staticmethod 
    def get_coordsys(model_view):
        
        from .stc_classes.coordsys import SpaceFrame, TimeFrame        
        from .mango.coordsys import PhotCoordSys, ColorFrame

        dmtype = model_view.get("dmtype")
        
        if dmtype == "coords:SpaceSys":
            return SpaceFrame.get_spaceframe(model_view)
        elif dmtype == "coords:TimeFrame":
            return TimeFrame(model_view)
        elif dmtype == "mango:stcextend.PhotCoordSys":
            return PhotCoordSys(model_view)
        elif dmtype == "mango:stcextend.ColorFrame":
            return ColorFrame(model_view)
        else:
            raise Exception(f"coordSys type {dmtype} not supported yet")
        
        
    @staticmethod 
    def get_error(model_view):
        from .stc_classes.error import Symmetrical, Ellipse, Bound2D, Bound3D, Asymmetrical2D, Asymmetrical3D
        dmtype = model_view.get("dmtype")
        if dmtype == "meas:Symmetrical":
            return Symmetrical(model_view)
        elif dmtype == "meas:Ellipse":
            return Ellipse(model_view)
        elif dmtype == "meas:Bound2D":
            return Bound2D(model_view)
        elif dmtype == "meas:Bound3D":
            return Bound3D(model_view)
        elif dmtype == "meas:Asymmetrical2D":
            return Asymmetrical2D(model_view)
        elif dmtype == "meas:Asymmetrical3D":
            return Asymmetrical3D(model_view)
        else:
            raise Exception(f"Error type {dmtype} not supported yet")
        return "error"

