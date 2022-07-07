'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..root_class import RootClass
from ..stc_classes.coordframe import CoordFrame
from ..photdm.photcal import PhotCal
from ..photdm.photfilter import PhotometryFilter
from mivot_code.utils.xml_utils import XmlUtils

class PhotFrame(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = "PhotFrame"
        self.dmtype = None
        self.photCal = None
        
        for ele in model_view.xpath('.//INSTANCE[@dmtype="photdm:PhotCal"]'):
            self.photCal = PhotCal(ele)
            break
        self.label  = self.photCal.label

    
class ColorFrame(CoordFrame):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        super().__init__(model_view)
        self.dmtype = "ColorFrame"
        self.low = None
        self.high = None

        self.low = PhotometryFilter(XmlUtils.get_instance_by_role(model_view, "mango:stcextend.HRFrame.low"))
        self.high = PhotometryFilter(XmlUtils.get_instance_by_role(model_view, "mango:stcextend.HRFrame.high"))
            
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
        super().__init__(model_view)
        self.dmtype = "FlagDictionnary"
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
    
    def get_label(self, value):
        if value in self.entries:
            return self.entries[value]
        return None
    


