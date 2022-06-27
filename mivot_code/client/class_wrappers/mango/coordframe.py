'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..stc_classes.coordframe import CoordFrame
from ..photdm.photcal import PhotCal
from ..photdm.photfilter import PhotometryFilter

class PhotFrame(CoordFrame):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = None
        self.photCal = None
        
        for ele in model_view.xpath('.//INSTANCE[@dmtype="photdm:PhotCal"]'):
            self.photCal = PhotCal(ele)
            break
        self.label  = self.photCal.label

    def __repr__(self):
        return self.label
    
class ColorFrame(CoordFrame):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.dmtype = None
        self.low = None
        self.high = None

        for ele in model_view.xpath('.//INSTANCE[@dmrole="mango:stcextend.HRFrame.low"]'):
            self.low = PhotometryFilter(ele)
        for ele in model_view.xpath('.//INSTANCE[@dmrole="mango:stcextend.HRFrame.high"]'):
            self.high = PhotometryFilter(ele)
            
        self.label  = f"{self.low.label}<>{self.high.label}"

    def __repr__(self):
        return self.label

 

