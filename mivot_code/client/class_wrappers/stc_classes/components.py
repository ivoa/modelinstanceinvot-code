'''
Created on 20 Jan 2022

@author: laurentmichel
'''
from mivot_code.utils.xml_utils import XmlUtils

class Quantity():
    
    def __init__(self, model_view):
        self.value = None
        self.unit =  ""
        # shortcut ivoa:Quantity as a simple ATTRIBUTE
        if model_view.tag == "ATTRIBUTE":
            value = model_view.get("value")
            try:
                self.value = float(value)
            except :
                self.value = float('NaN')
            self.unit = model_view.get("unit")
        else:
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

