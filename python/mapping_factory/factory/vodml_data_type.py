'''
Created on 20 avr. 2020

@author: laurentmichel
'''

from mapping_factory.factory.vodml_constraint_dict import VodmlConstraintDict


class VodmlDataType:

    def __init__(self, vodmlid, name, ref, superclass, attributes,
                 abstract=False, vodml_constraints=VodmlConstraintDict(),
                 literals={}):
        '''
        :param vodmlid:
        :type vodmlid:
        :param name:
        :type name:
        :param ref:
        :type ref:
        :param superclass:
        :type superclass:
        :param attributes:
        :type attributes:
        :param abstract:
        :type abstract:
        :param vodml_constraints:
        :type vodml_constraints: VodmlConstraintDict
        :param literals:
        :type literals: {vodml-id:{name, description}}
        '''
        self.vodmlid = vodmlid
        self.ref = ref
        self.name = name
        self.superclass = superclass
        self.attributes = attributes
        self.abstract = abstract
        self.vodml_constraints = vodml_constraints 
        self.literals = literals 
        
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        retour = ""
        if self.abstract:
            retour += "Abstract "
        retour += "DATATYPE " + self.name + " vodmlid=" + self.vodmlid + " ref" + self.ref 
        retour += "\n    ATTRIBUTES " + self.attributes.__repr__()
        retour += "\n    " + self.vodml_constraints.__repr__()
        return retour
    
