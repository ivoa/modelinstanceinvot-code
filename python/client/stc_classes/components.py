'''
Created on 20 Jan 2022

@author: laurentmichel
'''

class Quantity():
    
    def __init__(self, model_view):
        self.value = None
        self.unit =  ""
        for att in model_view.xpath('.//ATTRIBUTE'):
            dmrole = att.get("dmrole")
            value = att.get("value")
            if dmrole == "ivoa:Quantity.val":
                self.value = float(value)
            if dmrole == "ivoa:Quantity.unit":
                self.unit = value
                
    def __str__(self):
        return f"{self.value}{self.unit}"

