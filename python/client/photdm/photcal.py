'''
Created on 30 Jan 2022

@author: laurentmichel
'''
from .photfilter import PhotometryFilter

class PhotCal(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.identifier = None
        self.zeroPoint = None
        self.photometryFilter = None
        self.magnitudeSystem = None
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotCal.zeroPoint"]'):
            self.zeroPoint = ZeroPoint.get_zero_point(ele)
            break
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotCal.photometryFilter"]'):
            self.photometryFilter = PhotometryFilter(ele)
            break
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotCal.magnitudeSystem"]'):
            self.magnitudeSystem = MagnitudeSystem(ele)
            break
            
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotCal.identifier"]'):
            self.identifier = ele.get("value")
            break
        
    def __repr__(self):
        return f"{self.identifier}\n"\
            f"   magnitudeSystem {self.magnitudeSystem}\n"\
            f"   photometryFilter {self.photometryFilter}\n"\
            f"   zeroPoint {self.zeroPoint}\n"\
       
class MagnitudeSystem(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.type = None
        self.referencesSpectrum = None
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:MagnitudeSystem.type"]'):
            self.type = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:MagnitudeSystem.refererenceSpectrum"]'):
            self.referencesSpectrum = ele.get("value")
            break


    def __repr__(self):
        return f"ucd: {self.type} refSpectrum: {self.referencesSpectrum}"
    
    


class ZeroPoint(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.type = None
        self.referenceMagnitudeValue = None
        self.referenceMagnitudeError = None
        self.flux = None
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:ZeroPoint.type"]'):
            self.type = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:ZeroPoint.referenceMagnitudeValue"]'):
            self.referenceMagnitudeValue = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:ZeroPoint.referenceMagnitudeError"]'):
            self.referenceMagnitudeValue = float(ele.get("value"))
            break
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:ZeroPoint.flux"]'):
            self.flux = Flux(ele)
            break



    @staticmethod
    def get_zero_point(ele):
        dmtype = ele.get("dmtype")
        if dmtype is None:
            raise Exception(f"No type given for ZeroPoint")

        if dmtype == "photdm:PogsonZeroPoint":
            return PogsonZeroPoint(ele)
        elif dmtype == "photdm:LinearFluxZeroPoint":
            return LinearFluxZeroPoint(ele)
        elif dmtype == "photdm:AsinhZeroPoint":
            return AsinhZeroPoint(ele)
        raise Exception(f"ZeroPoint of type {dmtype} not supported")

    def __repr__(self):
        return f"type: {self.type} mag: {self.referenceMagnitudeValue} +/- {self.referenceMagnitudeError}\n"\
            f"flux: {self.flux}"
    
class PogsonZeroPoint(ZeroPoint):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        ZeroPoint.__init__(self, model_view)

    def __repr__(self):
        return f"PogsonZeroPoint : {ZeroPoint.__repr__(self)}"
    
class LinearFluxZeroPoint(ZeroPoint):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        ZeroPoint.__init__(self, model_view)

    def __repr__(self):
        return f"LinearFluxZeroPoint : {ZeroPoint.__repr__(self)}"
    
class AsinhZeroPoint(ZeroPoint):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        ZeroPoint.__init__(self, model_view)
        self.softeningParameter = None
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:ZeroPoint.softeningParameter"]'):
            self.softeningParameter = ele.get("value")
            break


    def __repr__(self):
        return f"AsinhZeroPoint : {ZeroPoint.__repr__(self)} softeningParameter:{self.softeningParameter}"
 
class Flux(object):
    
    def __init__(self, model_view):
        self.ucd= None
        self.unitexpression= None
        self.value = None
        self.error = None
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Flux.ucd"]'):
            self.ucd = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Flux.unitexpression"]'):
            self.unitexpression = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Flux.value"]'):
            self.value = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Flux.error"]'):
            self.error = float(ele.get("value"))
            break

    def __repr__(self):
        return f"ucd: {self.ucd} value:{self.value} +/- {self.error} {self.unitexpression}"