'''
Created on 20 avr. 2020

@author: laurentmichel
'''


class VodmlConstraintDict:    

    def __init__(self):
        self._constraints = dict()
        
    def __str__(self):
        retour = "CONSTRAINTS [ "
        for r, vc in self._constraints.items():
            retour += r + ": " + vc.__str__() + " "
        retour += "]"
        return retour
    
    def __repr__(self):
        return self.__str__()
    
    def add_contraint(self, vodml_contraint):
        if(vodml_contraint.is_empty):
            return
        if(isinstance(vodml_contraint, list)):
            raise Exception("===============")
        if vodml_contraint and not vodml_contraint.is_empty :
            att_role = vodml_contraint.att_role
            if att_role not in self._constraints.keys():
                self._constraints[att_role] = vodml_contraint
            else :
                ar = self._constraints[att_role]
                for st in vodml_contraint.subsets:
                    if st not in ar.subsets:
                        ar.add_subset(st) 
    
    @property
    def constraints(self):
        return self._constraints
    
    def keys(self):
        return self._constraints.keys()
    
    def merge(self, vodml_constraint_dict):
        for k, vodml_constraint in vodml_constraint_dict.constraints.items():
            if k not in self._constraints.keys():
                self._constraints[k] = vodml_constraint
            else:
                self.add_contraint(vodml_constraint)
