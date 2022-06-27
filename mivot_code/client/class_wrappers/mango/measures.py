'''
Created on 27 Jun 2022

@author: laurentmichel
'''
from ..stc_classes.measure import Measure

    
class Color(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)

    def __repr__(self):
        return self.label


class Photometry(Measure):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        Measure.__init__(self, model_view)

    def __repr__(self):
        return self.label
