'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from .components import Quantity 

class Error(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
    
    @staticmethod 
    def get_error(model_view):
        dmtype = model_view.get("dmtype")
        if dmtype == "meas:Ellipse":
            return Ellipse(model_view)
        else:
            raise Exception(f"Error type {dmtype} not supported yet")
        return "error"
    
class Ellipse(Error):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.semiaxis = []
        self.angle = None
        self.dmtype = "Ellipse"
        
        for ele in model_view.xpath('.//COLLECTION/INSTANCE'):
            self.semiaxis.append(Quantity(ele))
                
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Ellipse.posAngle"]'):
            self.angle = Quantity(ele)

    def __repr__(self):
        return f"[{self.dmtype}: [{self.semiaxis[0]} {self.semiaxis[0]}] {self.angle}]"