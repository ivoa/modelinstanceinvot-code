'''
Created on 20 avr. 2020

@author: laurentmichel
'''
from mapping_factory.factory.vodml_constraint_dict import VodmlConstraintDict


class VodmlObjectType:
    '''
    
    '''

    def __init__(self, vomdlid, name, superclass, attributes, abstract=False, vodml_constraints=VodmlConstraintDict()):
        self.vodmlid = vomdlid
        self.name = name
        self.superclass = superclass
        self.attributes = attributes
        self.abstract = abstract
        self.vodml_constraints = vodml_constraints
        
    def __str__(self):
        retour = ""
        if self.abstract:
            retour += "Abstract "
        retour += "OBJECT " 
        if self.superclass != '':
            retour += "(extends " + self.superclass + ") "
        retour += self.name + " " + self.vodmlid + "\nATTRIBUTES\n"
        for attribute in self.attributes.values():
            retour += " - " + attribute.__str__()
        retour += "CONSTRAINTS " + self.vodml_constraints.__repr__()
        return retour
    
    def __repr__(self):
        return self.__str__()
                     
