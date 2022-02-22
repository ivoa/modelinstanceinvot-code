'''
Created on 30 Jan 2022

@author: laurentmichel
'''

    
class PhotometryFilter(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
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
        for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotometryFilter.bandWidth"]'):
            self.bandWidh = BandWidth(ele)
            break
        for ele in model_view.xpath('.//INSTANCE[@dmrole="photdm:PhotometryFilter.transmissionCurve"]'):
            self.transmissionCurve = TransmissionCurve(ele)
            break

    def __repr__(self):
        return f"{self.fpsidentifier}/{self.identifier}/{self.name}/{self.bandname}  {self.description} valid from {self.dateValidityFrom} to {self.dateValidityTo}"\
            f"\nspectralLocation {self.spectralLocation}" \
            f"\nbandWidth {self.bandWidh}" \
            f"\ntransmissionCurve\n {self.transmissionCurve}" 
    
class SpectralLocation(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
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
        return f"ucd:{self.ucd} value:{self.value} {self.unitexpression}"
    
class BandWidth(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.ucd = None
        self.unitexpression = None
        self.extent = None
        self.start = None
        self.stop = None

        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:BandWidth.ucd"]'):
            self.ucd = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:BandWidth.unitexpression"]'):
            self.unitexpression = ele.get("value")
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:BandWidth.extent"]'):
            self.extent = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:BandWidth.start"]'):
            self.start = float(ele.get("value"))
            break
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="photdm:BandWidth.stop"]'):
            self.stop = float(ele.get("value"))
            break

    def __repr__(self):
        return f"ucd:{self.ucd} range:[{self.start} - {self.stop}] {self.extent} {self.unitexpression}"
      
class TransmissionCurve(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
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
        retour= f"access:{self.access}\ntransmissionPoint\n"
        for point in self.transmissionPoint:
            retour += f" {point}\n"
        return retour

        
class Access(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
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
        return f"reference:{self.reference} size:{self.size} format:{self.format}"
        
class TransmissionPoint(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
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
        return f"{self.ucd} spectra:{self.spectralValue} +/- {self.spectralError} {self.unit} -> {self.transmissionValue}"
   
      


