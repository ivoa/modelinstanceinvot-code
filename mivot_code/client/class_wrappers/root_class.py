'''
Created on 1 Jul 2022

@author: laurentmichel
'''
class RootClass(object):
    '''
    classdocs
    '''
    def __init__(self, model_view):
        self.label = 'NoSet'
        self.dmtype = 'NotSet'
        
    def __repr__(self):
        return self.label
