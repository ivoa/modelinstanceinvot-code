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

class FlagDictionnary(CoordFrame):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.entries = {}
        for coll in model_view.xpath('.//COLLECTION[@dmrole="mango:stcextend.Status.statusLabel"]'):
            for item in coll:
                value = None
                label = None
                for att in item.xpath('.//ATTRIBUTE[@dmrole="mango:stcextend.StatusLabel.value"]'):
                    value = att.get("value")
                for att in item.xpath('.//ATTRIBUTE[@dmrole="mango:stcextend.StatusLabel.label"]'):
                    label = att.get("value")
                self.entries[value] = label

        self.label  = "FlagDictionnary"

    def __repr__(self):
        return self.label
    
    def get_label(self, value):
        if value in self.entries:
            return self.entries[value]
        return None
    


