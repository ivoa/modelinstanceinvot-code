'''
Created on Jan 22, 2021

@author: laurentmichel
'''
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
        self.associated_data = None
        self._parse_and_check()
        
    def _parse_and_check(self):
        """
        Parse the mapping block
        Take the first data row as Mango object template
        """
        if self.table_mapper is None:
            self.table_mapper = self.vodml_instance.get_root_element("mango:MangoObject")
            if self.table_mapper is not None:
                self.mango_instance  = self.table_mapper._get_next_row_instance()
                if self.mango_instance is None:
                    self.table_mapper = None
                else:
                    self.table_mapper.rewind()
                    self.parameters = self.get_parameters()
                    self.associated_data = self.get_associated_data()
                    logger.info("Mango parser init")
            else :
                self.table_mapper = None
                

    def get_parameters(self, pretty_print=False):
        """
        Return all the mapped measures as a dict
        """
        if self.parameters is not None:
            return self.parameters
        self._parse_and_check()
        retour = {}
        
        retour["#0 meta.id;meta.main"] = self.get_mango_identifier()
        
        """
        Small tweak to deal different Mango versions
        """
        param_dock = "mango:MangoObject.parameterDock"
        if param_dock not in self.mango_instance:
            param_dock = "mango:MangoObject.parameters"
        
        cpt = 1
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
        """
        Return a data description of the current data row.
        data descrption {head, selected_index, data}
        - head: descriptor for each read column. 
                Contains the keys of the parameter descriptor returned by get_parameters
        - selected_index; Number of the read column ordered as for the head
        - data: read values ordered as for the head
        TODO so far we keep stuck to the first row
        """     
        retour = self._set_data_header(ucd, measure_type)
        if len(retour["selected_index"]) == 0:
            logger.error("No matching parameter found (ucd=%s, measure_type=%s", ucd, measure_type)
            return retour

        cpt = 0   
        # TO DO so far we keep stuck to the first row
        self.table_mapper.rewind()
        while True:
            inst = self.table_mapper._get_next_flatten_row()
            if inst is None:
                break
            row = []
            for ind in retour["selected_index"]:
                row.append(inst[ind])
            cpt += 1
            retour["data"].append(row)
            break

        logger.info("%s rows read", cpt)
        #retour.pop("selected_index")
        return retour

    
    def get_mango_identifier(self):
        """
        Return the Mango identifier as a measure {}
        """
        col_ref = { "measure_type": "mango:MangoObject.identifier",
                   "mango:MangoObject.identifier":{
                    "id": self.mango_instance["mango:MangoObject.identifier"]["@ref"],
                    "index" : self.table_mapper.column_mapping.get_mapping_index(self.mango_instance["mango:MangoObject.identifier"]["@ref"])
                    }
                }
        return col_ref        
 
    def get_associated_data(self, pretty_print=False):
        """
        Return all the mapped associated data as a dict
        """
        if self.associated_data is not None:
            return self.associated_data
        self._parse_and_check(
            )
        retour = {}
       
        if "mango:MangoObject.associatedDataDock" not in self.mango_instance:
            return retour
        
        cpt = 1
        for value in self.mango_instance["mango:MangoObject.associatedDataDock"]:
            associated_data_dict = self._get_associated_dict(value)
            
            key = "#{} {}". format(cpt, associated_data_dict["data_type"])
            retour[key] = associated_data_dict
            cpt += 1

        return retour
    
    
    def get_param_coordsys(self, param_key):
        """
        Returns the coordinate system of the parameter referenced by "key" in the parameter dict
        """
        if param_key not in  self.parameters:
            logger.error("No parameter attached to the key %s", param_key)
            return {}
        parameter = self.parameters[param_key]
        if "coosys_type" not in parameter:
            logger.info("parameter %s has no coosys_type", param_key)
            return {}

        return parameter[parameter["coosys_type"]]
    
    def _set_data_header(self, ucd, measure_type):
        
        retour = {
            "selected_index":[],
            "head": [],
            "data":[]
            }
        for pkey, value in self.parameters.items():
            if((ucd is None and measure_type is None)
                or (ucd is not None and pkey.endswith(ucd)) 
                or value["measure_type"] == measure_type):
                logger.info("got parameter [%s] selected with ucd=%s and measure_type=%s", pkey, ucd, measure_type)

                measure = value[value["measure_type"]]

                for axes_key, axe in measure.items():
                    self._get_measure_header(value, pkey, axe, axes_key, retour)
                    
                if "associatedParameters" in value:
                    for _, associated_parameter in value["associatedParameters"].items():
                        ap_measure = associated_parameter[associated_parameter["measure_type"]]
                        prefix = self._get_semantic_header(value) + "->"
                        for ap_axes_key, ap_axe in ap_measure.items():
                            self._get_measure_header(associated_parameter, ap_axe, ap_axes_key, retour, prefix=prefix)

                self._get_error_header(value, pkey, retour)      
 
        return retour
    
    def _get_semantic_header(self, parameter): 
        """
        Not used for now: using a redirection to the param description is better
        """  
        head = "("         
        if "ucd" in parameter.keys():
            head += parameter["ucd"] 
        if "semantic" in parameter.keys():
                head +=  " " +  parameter["semantic"] 
        if "description" in parameter.keys():
                head +=  " " +  parameter["description"] 
        head += ")"
        return head

    def _get_measure_header(self, parameter, measure_key, axe, axes_key, retour, prefix=""):
        """
        Set the fields head and selected_index of the data descriptor for measure
        """
        measure = parameter[parameter["measure_type"]]

        if isinstance(axe, dict):
            head = prefix + axes_key + " [" + measure_key  + "]"#self._get_semantic_header(parameter)
            retour["head"].append(head)
            retour["selected_index"].append(axe["index"])
        # measure values are direct children the measure element
        elif axes_key == "id" or axes_key == "index" and parameter["measure_type"] not in retour["head"]:
            head = parameter["measure_type"] + " ["  + measure_key + "]" # + self._get_semantic_header(parameter)
            retour["head"].append(parameter["measure_type"])
            retour["selected_index"].append(measure["index"])
        return retour
    
    def _get_error_header(self,parameter, measure_key, retour):
        if "error_type" in parameter.keys() :
            error_type = parameter["error_type"]
            errors = parameter[error_type]
            for key, ele in errors.items():
                if isinstance(ele, dict):
                    retour["head"].append("error: " + key + " [" + measure_key + "]")
                    retour["selected_index"].append(ele["index"])
        
    def _pretty_filter_parameter(self, parameter_dict):
        parameter_dict.pop("coord_type")
        parameter_dict.pop("measure_type")
        if parameter_dict["error_type"] is None:
            parameter_dict.pop("error_type")


    def _get_associated_dict(self, measure_node):
                                          
        if "mango:AssociatedData.description" not in measure_node:
            description = None
        else:
            description = self._get_element_value(measure_node["mango:AssociatedData.description"])
            
        if "mango:AssociatedData.semantic" not in measure_node:
            semantic = None
        else:
            semantic = self._get_element_value(measure_node["mango:AssociatedData.semantic"])
                  
        data_type = self._get_element_dmtype(measure_node)
        
        data = {}
        if data_type.endswith("WebEndpoint") is True:
            data["ContentType"] = measure_node["mango:WebEndpoint.contentType"]["@value"]
            data["url"] = measure_node["mango:WebEndpoint.uri"]["@value"]
                     
        retour = {"description": description,
                       "semantic": semantic,
                       "data_type": data_type,
                       data_type: data}
        
        return retour
        
    def _get_parameter_dict(self, root_node):
        # Should never occur with a clean mapping
        if "mango:Parameter.ucd" not in root_node:
            ucd = None
        else:
            ucd = self._get_element_value(root_node["mango:Parameter.ucd"])                         
                                          
        if "mango:Parameter.description" not in root_node:
            description = None
        else:
            description = self._get_element_value(root_node["mango:Parameter.description"])
            
        if "mango:Parameter.semantic" not in root_node:
            semantic = None
        else:
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
                    coosys_obj = coord_sys_obj
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
        """
        Build a readable description of one value of the measure 
        """
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
                    "index" : self.table_mapper.column_mapping.get_mapping_index(
                        measure_subelement["ivoa:RealQuantity.value"]["@ref"]
                        )
                    }
                retour["field:" + retour_key] = col_ref
            else:
                retour[retour_key] = measure_subelement["ivoa:RealQuantity.value"]["@value"] 

    
            unit = ""                            
            if "ivoa:Quantity.unit" in measure_subelement and "@value" in measure_subelement["ivoa:Quantity.unit"]:
                unit = measure_subelement["ivoa:Quantity.unit"]["@value"]
            if unit != "":
                retour["unit"] = unit
    
        elif   "@ref" in measure_subelement:
            col_ref = {
                    "id": measure_subelement["@ref"],
                    "index" : self.table_mapper.column_mapping.get_mapping_index(
                        measure_subelement["@ref"]
                        )
                }
            last = sub_key.split('.')[-1]
            retour["field:" + last] = col_ref

            unit = ""
            if "@unit" in measure_subelement:
                unit = measure_subelement["@unit"]
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

