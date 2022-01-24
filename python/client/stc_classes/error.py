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
        if dmtype == "meas:Symmetrical":
            return Symmetrical(model_view)
        elif dmtype == "meas:Ellipse":
            return Ellipse(model_view)
        elif dmtype == "meas:Bound2D":
            return Bound2D(model_view)
        elif dmtype == "meas:Bound3D":
            return Bound3D(model_view)
        else:
            raise Exception(f"Error type {dmtype} not supported yet")
        return "error"

class Symmetrical(Error):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.radius = None
        self.dmtype = "Symmetrical"
                
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Symmetrical.radius"]'):
            self.radius = Quantity(ele)

    def __repr__(self):
        return f"[{self.dmtype}: [{self.radius}]]"  
    
      
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
        return f"[{self.dmtype}: [{self.semiaxis[0]} {self.semiaxis[1]}] {self.angle}]"

class Bound2D(Error):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.loLimit = []
        self.hiLimit = []
        self.dmtype = "Bound2D"
        
        for ele in model_view.xpath('.//COLLECTION[@dmrole="meas:Bounds2D.loLimit"]/INSTANCE'):
            self.loLimit.append(Quantity(ele))
            
        for ele in model_view.xpath('.//COLLECTION[@dmrole="meas:Bounds2D.hiLimit"]/INSTANCE'):
            self.hiLimit.append(Quantity(ele))
                

    def __repr__(self):
        return f"[{self.dmtype}: ["\
            f"[{self.loLimit[0].value} {self.hiLimit[0].value}]{self.hiLimit[0].unit} "\
            f"[{self.loLimit[1].value} {self.hiLimit[1].value}]{self.hiLimit[1].unit} ]"   
    
class Bound3D(Error):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.loLimit = []
        self.hiLimit = []
        self.dmtype = "Bound3D"
        
        for ele in model_view.xpath('.//COLLECTION[@dmrole="meas:Bounds3D.loLimit"]/INSTANCE'):
            self.loLimit.append(Quantity(ele))
            
        for ele in model_view.xpath('.//COLLECTION[@dmrole="meas:Bounds3D.hiLimit"]/INSTANCE'):
            self.hiLimit.append(Quantity(ele))
                

    def __repr__(self):
        return f"[{self.dmtype}: ["\
            f"[{self.loLimit[0].value} {self.hiLimit[0].value}]{self.hiLimit[0].unit} "\
            f"[{self.loLimit[1].value} {self.hiLimit[1].value}]{self.hiLimit[1].unit} "\
            f"[{self.loLimit[2].value} {self.hiLimit[2].value}]{self.hiLimit[2].unit}]"