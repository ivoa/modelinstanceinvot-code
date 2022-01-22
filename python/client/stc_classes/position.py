'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from .error import Error
from .point import Point

class Position(object):
    '''
    classdocs
    '''


    def __init__(self, model_view):
        '''
        Constructor
        '''
        self.coord = None
        self.error = None
        self.ucd = None
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Measure.error"]'):
            self.error = Error.get_error(ele)
            break
            
        for ele in model_view.xpath('.//ATTRIBUTE[@dmrole="meas:Position.ucd"]'):
            self.ucd = ele.get("value")
            break
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="meas:Position.coord"]'):
            self.coord = Point.get_point(ele)
            break

        

        