'''
Created on Jan 22, 2021

Mist be split o 2 parts : one generic and one mamgo specific
@author: laurentmichel
'''
from numpy.testing._private.utils import measure


class InstanceBrowser(object):
    '''
    classdocs
    '''

    def __init__(self, json_instance):
        '''
        Constructor
        '''
        self.json_instance = json_instance
    
    def get_identifier(self):
        return   self.json_instance["mango:MangoObject.identifier"]["@value"]
        
    def get_parameter_list(self):
        retour = {}
        cpt = 1
        for value in self.json_instance["mango:MangoObject.parameters"]:
            ucd = self._get_element_value(value["mango:Parameter.ucd"])
            key = "#{} {}". format(cpt, ucd)
            description = self._get_element_value(value["mango:Parameter.description"])
            semantic = self._get_element_value(value["mango:Parameter.semantic"])
            dmtype = self._get_element_dmtype(value["mango:Parameter.measure"])
            errortype = self._get_element_dmtype(value["mango:Parameter.measure"]["meas:Measure.error"])
            coord_type = self._get_measure_coord_type(value["mango:Parameter.measure"])
            retour[key] = {"ucd": ucd,
                           "description": description,
                           "semantic": semantic,
                           "measure_type": dmtype,
                           "error_type": errortype,
                           "coord_type": coord_type}
            cpt += 1
        return retour
        
    def _get_element_value(self, element):
        if "@value" in element:
            return element["@value"]
        else:
            return None
    
    def _get_element_dmtype(self, element):
        if "@dmtype" in element:
            return element["@dmtype"]
        else:
            return None
        
    def _get_measure_coord_type(self, measure_element):
        dmtype = self._get_element_dmtype(measure_element)
        for key in measure_element.keys():
            print(dmtype + " " + key)
            if key.startswith(dmtype):
                return self._get_element_dmtype(measure_element[key])
        return None
