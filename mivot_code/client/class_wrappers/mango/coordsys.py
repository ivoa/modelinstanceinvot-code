'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..stc_classes.coordsys import PhysicalCoordSys
from ..photdm.photcal import PhotCal
from ..photdm.photfilter import PhotometryFilter

class PhotCoordSys(PhysicalCoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.dmtype = "PhotCoordSys"
        self.dmtype = None
        self.photCal = None
        
        for ele in model_view.xpath('.//INSTANCE[@dmtype="photdm:PhotCal"]'):
            self.photCal = PhotCal(ele)
            break
        self.label  = self.photCal.label
    
class ColorFrame(PhysicalCoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.dmtype = "ColorFrame"
        self.dmtype = None
        self.low = None
        self.high = None

        for ele in model_view.xpath('.//INSTANCE[@dmrole="mango:stcextend.HRFrame.low"]'):
            self.low = PhotometryFilter(ele)
        for ele in model_view.xpath('.//INSTANCE[@dmrole="mango:stcextend.HRFrame.high"]'):
            self.high = PhotometryFilter(ele)
            
        self.label  = f"{self.low.label}<>{self.high.label}"

 

