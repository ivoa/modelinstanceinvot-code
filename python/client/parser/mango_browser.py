'''
Created on Jan 22, 2021

@author: laurentmichel
'''
import sys
from utils.dict_utils import DictUtils
from client.inst_builder.vodml_instance import VodmlInstance
from client.parser import logger

class MangoBrowser(object):
    '''
    Provides a few methods helping for browsing JSON serialization of a MANGO mapping blocks
    '''

    def __init__(self, votable_path):
        '''
        Constructor
        '''
    
        self.vodml_instance = VodmlInstance(votable_path)
        self.vodml_instance.populate_templates(resolve_dmrefs=True)
        self.vodml_instance.connect_join_iterators()
        self.table_mapper = None
        self.mango_instance = None
        self.parameters = None
        self._parse_and_check()
        
    def _parse_and_check(self):
        if self.table_mapper is None:
            self.table_mapper = self.vodml_instance.get_root_element("mango:MangoObject")
            if self.table_mapper is not None:
                self.mango_instance  = self.table_mapper._get_next_row_instance()
                if self.mango_instance is None:
                    self.table_mapper = None
                else:
                    self.table_mapper.rewind()
                    self.parameters = self.get_parameters()
                    logger.info("Mango parser init")
            else :
                self.table_mapper = None

                

    def get_parameters(self, pretty_print=False):
        
        if self.parameters is not None:
            return self.parameters
        self._parse_and_check(
            )
        retour = {}
        cpt = 1
        
        param_dock = "mango:MangoObject.parameterDock"
        if param_dock not in self.mango_instance:
            param_dock = "mango:MangoObject.parameters"
            
        for value in self.mango_instance[param_dock]:
            parameter_dict = self._get_parameter_dict(value)
            if pretty_print is True:
                self._pretty_filter_parameter(parameter_dict)
            if  "mango:MangoObject.Parameter.associatedParameters" in value:
                apcpt = 1
                ap_dict = {}
                for associated_parameter in value["mango:MangoObject.Parameter.associatedParameters"]:
                    associated_parameter_dict = self._get_parameter_dict(associated_parameter)
                    if pretty_print is True:
                        self._pretty_filter_parameter(associated_parameter_dict)

                    key = "#{} {}". format(apcpt, associated_parameter_dict["ucd"])
                    ap_dict[key] = associated_parameter_dict
                    apcpt += 1
                if ap_dict != {}:
                    parameter_dict["associatedParameters"] = ap_dict
            key = "#{} {}". format(cpt, parameter_dict["ucd"])
            retour[key] = parameter_dict
            cpt += 1
        return retour

    def get_data(self, ucd=None, measure_type=None):
        retour = {
            "head": [],
            "data":[]
            }
        cpt = 0   
        ucd_found = False   
        for key, value in self.parameters.items():
            if ((ucd is not None and key.endswith(ucd)) 
                or value["measure_type"] == measure_type):
                logger.info("got parameter [%s] ucd=%s measure_type=%s", key, ucd, measure_type)

                measure_type = value["measure_type"]
                measure = value[measure_type]
                selected_index = []
                for key, ele in measure.items():
                    if isinstance(ele, dict):
                        retour["head"].append(key)
                        selected_index.append(ele["index"])
                        
                if "error_type" in value.keys() :
                    error_type = value["error_type"]
                    errors = value[error_type]
                    for key, ele in errors.items():
                        if isinstance(ele, dict):
                            retour["head"].append("error: " + key)
                            selected_index.append(ele["index"])

                ucd_found = True       
                self.table_mapper .rewind()
                while True:
                    inst = self.table_mapper._get_next_flatten_row()
                    if inst is None:
                        break
                    row = []
                    for ind in selected_index:
                        row.append(inst[ind])
                    cpt += 1
                    retour["data"].append(row)
        if ucd_found is False:
            logger.error("parameter %s not found", ucd)
        else:
            logger.info("%s rows read", cpt)
        return retour

                

    
    def get_identifier(self):
        return   self.mango_instance["mango:MangoObject.identifier"]["@value"]
 
    def get_associated_data_list(self, pretty_print=False):
        retour = {}
        cpt = 1
       
        if "mango:MangoObject.associatedDataDock" not in self.mango_instance:
            return retour
        
        for value in self.mango_instance["mango:MangoObject.associatedDataDock"]:
            print(DictUtils.get_pretty_json(value))
            import sys
            sys.exit()
            parameter_dict = self._get_parameter_dict(value)
            if pretty_print is True:
                self._pretty_filter_parameter(parameter_dict)
            if  "mango:MangoObject.Parameter.associatedParameters" in value:
                apcpt = 1
                ap_dict = {}
                for associated_parameter in value["mango:MangoObject.Parameter.associatedParameters"]:
                    associated_parameter_dict = self._get_parameter_dict(associated_parameter)
                    if pretty_print is True:
                        self._pretty_filter_parameter(associated_parameter_dict)

                    key = "#{} {}". format(apcpt, associated_parameter_dict["ucd"])
                    ap_dict[key] = associated_parameter_dict
                    apcpt += 1
                if ap_dict != {}:
                    parameter_dict["associatedParameters"] = ap_dict
            key = "#{} {}". format(cpt, parameter_dict["ucd"])
            retour[key] = parameter_dict
            cpt += 1
        return retour
        
    def get_parameter_list(self, pretty_print=False):
        retour = {}
        cpt = 1
        
        param_dock = "mango:MangoObject.parameterDock"
        if param_dock not in self.mango_instance:
            param_dock = "mango:MangoObject.parameters"
            
        for value in self.mango_instance[param_dock]:
            parameter_dict = self._get_parameter_dict(value)
            if pretty_print is True:
                self._pretty_filter_parameter(parameter_dict)
            if  "mango:MangoObject.Parameter.associatedParameters" in value:
                apcpt = 1
                ap_dict = {}
                for associated_parameter in value["mango:MangoObject.Parameter.associatedParameters"]:
                    associated_parameter_dict = self._get_parameter_dict(associated_parameter)
                    if pretty_print is True:
                        self._pretty_filter_parameter(associated_parameter_dict)

                    key = "#{} {}". format(apcpt, associated_parameter_dict["ucd"])
                    ap_dict[key] = associated_parameter_dict
                    apcpt += 1
                if ap_dict != {}:
                    parameter_dict["associatedParameters"] = ap_dict
            key = "#{} {}". format(cpt, parameter_dict["ucd"])
            retour[key] = parameter_dict
            cpt += 1
        return retour
    
    def _pretty_filter_parameter(self, parameter_dict):
        parameter_dict.pop("coord_type")
        parameter_dict.pop("measure_type")
        if parameter_dict["error_type"] is None:
            parameter_dict.pop("error_type")

        
    def _get_parameter_dict(self, root_node):
        ucd = self._get_element_value(root_node["mango:Parameter.ucd"])
        description = self._get_element_value(root_node["mango:Parameter.description"])
        semantic = self._get_element_value(root_node["mango:Parameter.semantic"])
        parameter_measure = root_node["mango:Parameter.measure"]
        dmtype = self._get_element_dmtype(parameter_measure)
        errortype = None
        error_values = {}
        if "meas:Measure.error" in parameter_measure:
            errortype = self._get_element_dmtype(parameter_measure["meas:Measure.error"])
            error_values = self._get_measure_coord_values(parameter_measure["meas:Measure.error"])
        coord_type = self._get_measure_coord_type(parameter_measure)
        values = self._get_measure_coord_values(parameter_measure)       
        coosys_type, coosys_obj = self._get_measure_coordsys_type(parameter_measure)
        
        retour = {"ucd": ucd,
                       "description": description,
                       "semantic": semantic,
                       "measure_type": dmtype,
                       #"error_type": errortype,
                       "coord_type": coord_type,
                       dmtype: values}
        
        if coosys_type != None :
            retour["coosys_type"] = coosys_type
            retour[coosys_type] = coosys_obj
            
        if errortype is not None:
            retour["error_type"] = errortype
            retour[errortype] = error_values
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
        #dmtype = self._get_element_dmtype(measure_element)
        for key in measure_element.keys():
            if key.startswith("meas:") or key.startswith("mango:"):
                return self._get_element_dmtype(measure_element[key])
        return None
    
    def _get_measure_coordsys_type(self, measure_element):
        #dmtype = self._get_element_dmtype(measure_element)
        for key in measure_element.keys():
            if key.startswith("meas:") or key.startswith("mango:"):
                if "coords:Coordinate.coordSys" in measure_element[key].keys():
                    coord_sys_obj = measure_element[key]["coords:Coordinate.coordSys"]
                    coosys_type = coord_sys_obj["@dmtype"]
                    coosys_obj = None
                    for cookey in coord_sys_obj.keys():
                        if cookey.endswith(".frame"):
                            coosys_obj = coord_sys_obj[cookey]
                    return coosys_type, coosys_obj
        return None, None
    
    def _get_measure_coord_values(self, measure_element):
        retour = {}
        for key in measure_element.keys():
            measure_comp = measure_element[key]

            if isinstance(measure_comp, dict) is True:    
                for sub_key in measure_comp.keys():
                    measure_subcomp = measure_comp[sub_key]
                    if isinstance(measure_subcomp, dict):
                        if isinstance(retour, list) is True:
                            retour = self.list_to_dict(retour)
                        retour.update(self._get_measure_coord_value(key, sub_key, measure_subcomp).items()) 

                    elif isinstance(measure_subcomp, list):
                        retour=[]
                        for item in measure_subcomp:
                            retour.append(self._get_measure_coord_value(key, sub_key, item))
        return retour
    
    def _get_measure_coord_value(self, key, sub_key, measure_subelement):
        retour = {}

        # Bypass the RealQuantity object to avoid values referenced as ivoa:real
        if "@dmtype" in measure_subelement and measure_subelement["@dmtype"].startswith("ivoa:RealQuantity"):
            # Bypass the coords:PhysicalCoordinate object which is meaning less
            if sub_key.endswith(".cval"):
                retour_key = key
            else:
                retour_key = sub_key
                  
            if "@ref" in measure_subelement["ivoa:RealQuantity.value"]:
                col_ref = {
                    "id": measure_subelement["ivoa:RealQuantity.value"]["@ref"],
                    "index" : self.table_mapper.column_mapping.get_mapping_index(measure_subelement["ivoa:RealQuantity.value"]["@ref"])
                    }
                retour["field:" + retour_key] = col_ref
            else:
                retour[retour_key] = measure_subelement["ivoa:RealQuantity.value"]["@value"] 

    
            unit = ""                            
            if "@value" in measure_subelement["ivoa:Quantity.unit"]:
                unit = measure_subelement["ivoa:Quantity.unit"]["@value"]
            if unit != "":
                retour["unit"] = unit
    
        elif   "@value" in measure_subelement:
            unit = ""
            if "@unit" in measure_subelement:
                unit = measure_subelement["@unit"]
            last = sub_key.split('.')[-1]
            retour[last] = measure_subelement["@value"] 
            if unit != "":
                retour["unit"] = unit
                
        return retour
    
    
    def list_to_dict(self, litem_list):
        nretour = {}
        cpt = 0
        for item in litem_list:
            for k, v in item.items():
                if isinstance(v, dict) is True:
                    nretour["#" + str(cpt) + " " + k] = v
                else:
                    nretour["#" + str(cpt) + " " + k] = v
            cpt += 1
        return nretour

