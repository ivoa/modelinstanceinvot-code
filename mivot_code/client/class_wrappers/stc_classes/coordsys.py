'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from ..root_class import RootClass
from ..component_builder import ComponentBuilder

class PhysicalCoordSys(RootClass):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        RootClass.__init__(self, model_view)
        self.dmtype = None
        
        for ele in model_view.xpath('.//INSTANCE[@dmrole="coords:PhysicalCoordSys.frame"]'):
            self.frame = ComponentBuilder.get_coordframe(ele)
        self.label = f"{self.frame.label}"

        
class SpaceSys(PhysicalCoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        PhysicalCoordSys.__init__(self, model_view)

class TimeSys(PhysicalCoordSys):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        '''
        Constructor
        '''
        PhysicalCoordSys.__init__(self, model_view)

