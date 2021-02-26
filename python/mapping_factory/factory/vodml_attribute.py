'''
Created on 20 avr. 2020

@author: laurentmichel
'''
from mapping_factory import logger


class VodmlAttribute:    

    def __init__(self, vodmlid, name, dmtype, array_size, is_reference):
        self.vodmlid = vodmlid
        self.name = name
        self.dmtype = dmtype
        self.array_size = array_size
        self.is_reference = is_reference
        self.already_mapped = False
        if dmtype == "":
            logger.info(name + " " + vodmlid + " has not dmtype")

    def __str__(self):
        retour = "ATTRIBUTE "
        retour += "(array_size " + str(self.array_size) + ") "
        retour += self.name + " " + self.vodmlid + " dmtype=" + self.dmtype.__str__()
        return retour

    def __repr__(self):
        return self.__str__()
    
