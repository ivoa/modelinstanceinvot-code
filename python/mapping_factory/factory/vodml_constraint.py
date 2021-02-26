'''
Created on 20 avr. 2020

@author: laurentmichel
'''


class VodmlConstraint:    

    def __init__(self, att_role):
        self._att_role = att_role
        self._subsets = []
        
    def __str__(self):
        retour = "CONSTRAINT "
        retour += self._att_role + "=>" + str(self._subsets)
        return retour
    
    def add_subset(self, subset):
        if not subset in self._subsets:
            self._subsets.append(subset)
            
    def add_constraint(self, vodmlcontraint):
        datatypes = vodmlcontraint.subsets
        for dt in datatypes:
            self.add_subset(dt)
            
    def __repr__(self):
        return self.__str__()
    
    @property
    def att_role(self):
        return self._att_role
    
    @property
    def subsets(self):
        return self._subsets
    
    @property
    def is_empty(self):
        return True if len(self._subsets) == 0  else False
    
    @property
    def is_single(self):
        return True if len(self._subsets) == 1  else False

    @property    
    def length(self):
        return len(self._subsets)        
