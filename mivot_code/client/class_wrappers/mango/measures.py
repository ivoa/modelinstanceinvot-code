'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..stc_classes.measures import Measure

    
class Color(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.dmtype = "Color"


class Flag(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.dmtype = "Flag"


class Photometry(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)
        self.measure = "Photometry"
