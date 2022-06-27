'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from mivot_code.utils.xml_utils import XmlUtils

class Quantity():
    
    def __init__(self, model_view):
        self.value = None
        self.unit =  ""
        for att in model_view.xpath('.//ATTRIBUTE'):
            dmrole = att.get("dmrole")
            value = att.get("value")
            if (
                dmrole == "ivoa:RealQuantity.value" or dmrole == "ivoa:Quantity.value" or
                dmrole == "ivoa:RealQuantity.val" or dmrole == "ivoa:Quantity.val" ):
                try:
                    self.value = float(value)
                except :
                    self.value = float('NaN')

            if dmrole == "ivoa:RealQuantity.unit" or dmrole == "ivoa:Quantity.unit":
                self.unit = value
        self.label = f"{self.value} {self.unit}"
                
    def __str__(self):
        return self.label

