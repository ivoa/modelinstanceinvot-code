'''
Created on 30 Jan 2022

@author: laurentmichel
'''
from ..root_class import RootClass
from mivot_code.utils.xml_utils import XmlUtils

    
class PhotometryFilter(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = "Flux"
        self.fpsidentifier = None
        self.identifier = None
        self.name = None
        self.description = None
        self.bandname = None
        self.dateValidityFrom = None
        self.dateValidityTo = None
        
        self.spectralLocation = None
        self.bandwidth = None
        self.transmissionCurve = None
        self.label = None

        if model_view is not None:

            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotometryFilter.fpsidentifier"]'):
                self.fpsidentifier = ele.get("value")
                break
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotometryFilter.identifier"]'):
                self.identifier = ele.get("value")
                break
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotometryFilter.name"]'):
                self.name = ele.get("value")
                break
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotometryFilter.description"]'):
                self.description = ele.get("value")
                break
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotometryFilter.bandname"]'):
                self.bandname = ele.get("value")
                break
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotometryFilter.dateValidityFrom"]'):
                self.dateValidityFrom = ele.get("value")
                break
            for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:PhotometryFilter.dateValidityTo"]'):
                self.dateValidityTo = ele.get("value")
                break
            for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotometryFilter.spectralLocation"]'):
                self.spectralLocation = SpectralLocation(ele)
                break
            for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotometryFilter.bandwidth"]'):
                self.bandwidth = Bandwidth(ele)
                break
            for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotometryFilter.transmissionCurve"]'):
                self.transmissionCurve = TransmissionCurve(ele)
                break
    
            self.label = self.identifier

    def __repr__(self):
        retour = f"== PhotometryFilter =====\n"\
                 f"  fpsidentifier: {self.fpsidentifier}\n"\
                 f"  identifier: {self.identifier}\n"\
                 f"  name: {self.name}\n"\
                 f"  bandname: {self.bandname}\n"\
                 f"  bandwidth: {self.bandwidth}\n"\
                 f"  description: {self.description}\n"\
                 f"  dateValidityFrom: {self.dateValidityFrom}\n"\
                 f"  dateValidityTo: {self.dateValidityTo}\n"
        if self.spectralLocation is not None:
            retour += f"  {self.spectralLocation}"
        if self.bandwidth is not None:
            retour += f"  {self.bandwidth}"
        if self.transmissionCurve is not None:
            retour += f"  {self.transmissionCurve}"
        return retour
    
class SpectralLocation(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = "SpectralLocation"
        self.ucd = None
        self.unitexpression = None
        self.value = None

        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:SpectralLocation.ucd"]'):
            self.ucd = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:SpectralLocation.unitexpression"]'):
            self.unitexpression = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:SpectralLocation.value"]'):
            self.value = float(ele.get("value"))
            break

    def __repr__(self):
        return f"== SpectralLocation =====\n"\
               f"  ucd:{self.ucd}\n"\
               f"  value:{self.value} {self.unitexpression}\n"
    
class Bandwidth(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = "Bandwidth"
        self.ucd = None
        self.unitexpression = None
        self.extent = None
        self.start = None
        self.stop = None
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Bandwidth.ucd"]'):
            self.ucd = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Bandwidth.unitexpression"]'):
            self.unitexpression = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Bandwidth.extent"]'):
            self.extent = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Bandwidth.start"]'):
            self.start = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Bandwidth.stop"]'):
            self.stop = float(ele.get("value"))
            break

    def __repr__(self):
        return f"== Bandwidth =====\n"\
               f"  ucd:{self.ucd}\n"\
               f"  start-stop:[{self.start} to {self.stop}]\n"\
               f"  extent: {self.extent}\n"\
               f"  unitexpression: {self.unitexpression}\n"
      
class TransmissionCurve(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = "TransmissionCurve"
        self.transmissionPoint = []
        self.access = None
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:TransmissionCurve.access"]'):
            self.access = Access(ele)
            break
        for ele in model_view.xpath('.//COLLECTION[@dmrole="photdm:TransmissionCurve.transmissionPoint"]'):
            for ele in ele.xpath('.//INSTANCE[@dmtype="photdm:TransmissionPoint"]'):
                self.transmissionPoint.append(TransmissionPoint(ele))
            break
     
    def __repr__(self):
        retour= f"== TransmissionCurve =====\n"
        if self.access is not None:
            retour += f"  {self.access}"
        retour += f"  transmissionPoint:\n"
        for point in self.transmissionPoint:
            retour += f"   {point}"
        return retour

        
class Access(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = "Access"
        self.reference = None
        self.size = None
        self.format = None
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Access.reference"]'):
            self.reference = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Access.size"]'):
            self.size = int(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:Access.format"]'):
            self.format = ele.get("value")
            break

    def __repr__(self):
        return f"== Access =====\n"\
               f"  reference:{self.reference}\n"\
               f"  size:{self.size}\n"\
               f"  format:{self.format}\n"
        
class TransmissionPoint(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = "TransmissionPoint"
        self.ucd = None
        self.unit = None
        self.transmissionValue = None
        self.spectralValue = None
        self.spectralError = None
        
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:TransmissionPoint.ucd"]'):
            self.ucd = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:TransmissionPoint.unit"]'):
            self.unit = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:TransmissionPoint.transmissionValue"]'):
            self.transmissionValue = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:TransmissionPoint.spectralValue"]'):
            self.spectralValue = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:TransmissionPoint.spectralError"]'):
            self.spectralError = float(ele.get("value"))
            break

    def __repr__(self):
        return f"{self.ucd} spectra:{self.spectralValue} +/- {self.spectralError} {self.unit} -> {self.transmissionValue}\n"
   
      


