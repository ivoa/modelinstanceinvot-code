'''
Created on 31 mars 2020

@author: laurentmichel
'''
import json, re
from astropy.io.votable import parse_single_table  
from client import logger
from client.objectbuilder.column_mapping import ColumnMapping
from client.objectbuilder.table_iterator import TableIterator
from client.objectbuilder.join_iterator import JoinIterator
from client.objectbuilder.row_filter import RowFilter
from client.objectbuilder import json_block_extractor, join_iterator
from client.objectbuilder.json_block_extractor import JsonBlockExtractor
from client.objectbuilder.att_utils import AttUtils
from client.translator.vocabulary import Ele,Att
from copy import deepcopy
from utils.dict_utils import DictUtils
from utils.json_tools import JsonTools


class TableMapper(object):
    '''
    classdocs
    '''

    def __init__(self,
                 table_name,
                 votable_path,
                 parsed_table=None,
                 json_inst_path=None ,
                 json_inst_dict=None):
        '''
        Constructor
        '''
        self.table_name = table_name
        self.parsed_table_path = votable_path
        if parsed_table is None:
            logger.info("take the first table")
            self.parsed_table = parse_single_table(self.parsed_table_path)
        else:
            logger.info("take the given parsed table")
            self.parsed_table = parsed_table
            
        self.table = self.parsed_table.to_table()
        
        if json_inst_path is not None:
            self.json_path = json_inst_path
            with open(self.json_path) as json_file:
                self.json = json.load(json_file)
        else:
            self.json = json_inst_dict
            self.json_path = None
            
        # mapping subset corresponding the  TABLE_MAPPING  
        self.table_json = self.json[Ele.VODML][Ele.TEMPLATES][self.table_name]
        # array block reference 
        self.array = None
        # key = role of the instance contained TABLE_ROW_TEMPLATE value = TableIterator
        self.table_iterators = {}
        self.column_mapping = ColumnMapping()
        # key = foreign table name value = TableIterator
        self.join_iterators = {}
        self.join = None
        # replace groupby with a suite of collection (one for each different key value
        

        
    def _set_header_values(self, root_element):
        """
        The term header refers to the model leaves that must be set with <PARAM> values
        Recursive function
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    self._set_header_values(root_element[idx])
        elif isinstance(root_element, dict):
            for k, v in root_element.items():
                # TODO For now PARAMS references in TABLE_ROW_TEMPLATE are not supported
                if k == 'TABLE_ROW_TEMPLATE':
                    pass
                else:
                    if isinstance(v, list):
                        for ele in v:
                            self._set_header_values(ele)
                    elif isinstance(v, dict):  
                        self._resolve_header_value(v)
                        self._set_header_values(v)

    def _set_table_iterators(self, root_element):
        """
        Build and array iterator for each TABLE_ROW_TEMPLATE element found within root_element
        """
        row_filter=None
        for key, value in root_element.items():
            if key == Ele.WHERE:
                row_filter = RowFilter(value)
                logger.info("TODO add more than one where statement")
            elif key.startswith("@") is False:
                self.array = value 
                iterator_key = self.table_name + "_" + key
                logger.info("Add table mapper %s", iterator_key)
                self.table_iterators[key] = TableIterator(
                                iterator_key,
                                self.parsed_table.to_table(),
                                value,
                                self.column_mapping,
                                row_filter=row_filter
                                ) 
    
    def _set_join_iterators(self, root_element):

        if isinstance(root_element, list):
            if JsonTools.is_join(root_element):
                # will be processed later as a dict
                pass
            for idx, _ in enumerate(root_element):
                self._set_join_iterators(root_element[idx])
        elif isinstance(root_element, dict):
            if JsonTools.is_join(root_element):
                join_iterator = JoinIterator(root_element)
                if join_iterator.foreign_table not in self.join_iterators:
                    self.join_iterators[join_iterator.foreign_table] = join_iterator
                else:
                    logger.error("more that 1 join iterators  on table % (only one is supported", join_iterator.foreign_table)
            else :
                for key, value in root_element.items():
                    if key.startswith("@") is False:
                        self._set_join_iterators(value) 

    def _set_array_subelement_values(self, array_element, parent_role=None, parent_type=None):
        """
        Recursive function
        Takes all @ref of the array_element content and map them the table columns
        """
        if isinstance(array_element, list):
            # Join content refers to others tables, 
            # it is processed the the join_iterator 
            if JsonTools.is_join(array_element) is True:
                return

            for idx, idv in enumerate(array_element):
                if self.retour is None:
                    prole = ""
                    ptype = ""
                    if "@dmrole" in idv:
                        prole = idv["@dmrole"]
                    if "@dmtype" in idv:
                        ptype = idv["@dmtype"]
                    self._set_array_subelement_values(array_element[idx], parent_role=prole, parent_type=ptype)
        elif isinstance(array_element, dict):
            for k, v in array_element.items():
                if isinstance(v, list):
                    # Join content refers to others tables, 
                    # it is processed the the join_iterator 
                    if JsonTools.is_join(v) is True:
                        continue
                    for ele in v:
                        prole = ""
                        ptype = ""
                        if "@dmrole" in ele:
                            prole = ele["@dmrole"]
                        if "@dmtype" in ele:
                            ptype = ele["@dmtype"]
                        if ptype.startswith("ivoa:"):
                            ptype = parent_type
                        self._set_array_subelement_values(ele, parent_role=prole, parent_type=ptype)
                elif isinstance(v, dict): 
                    ptype = ""
                    if "@dmtype" in v:
                        ptype = v["@dmtype"]
                    if ptype.startswith("ivoa:"):
                        ptype = parent_type
                    self._set_value(v, role=k, parent_role=parent_role, parent_type=ptype)
                    self._set_array_subelement_values(v, parent_role=k, parent_type=ptype)
   
    
    def _set_value(self, element, role=None, parent_role=None, parent_type=None):
        """
        Create a column mapping entry for the element if it is a @ref
        both role an parent_role are just labels used make to more explicit 
        the string representation of the columns mapping
        """
        keys = element.keys()
        if (Att.dmtype in keys and "@ref" in keys 
            and "@value" in keys and element["@value"] == ""):  
            logger.info("Give role %s to the column %s "
                        , role, element["@ref"])
            self.column_mapping.add_entry(element["@ref"]
                                          , role
                                          , parent_role=parent_role , parent_type=parent_type)
            element["@value"] = "array coucou"

    def _resolve_header_value(self, element):
        """
        Set the @value of element with the value of the <PARAM> having 
        either a ID or a name matching @ref 
        """
        keys = element.keys()
        if ("@dmtype" in keys and "@ref" in keys 
            and "@value" in keys and element["@value"] == ""):  
            for param in  self.parsed_table.params:
                if param.ID == element["@ref"]:
                    logger.info("set element %s with value=%s of PARAM(ID=%s)"
                                , str(element), param.value, element["@ref"])
                    # element["@value"] = param.value.decode("utf-8") 
                    try:
                        element["@value"] = param.value.decode("utf-8") 
                    except (UnicodeDecodeError, AttributeError):
                        element["@value"] = param.value

                elif param.name == element["@ref"] :
                    logger.info("set element%s with value=%s of PARAM(name=%s)"
                                , str(element), param.value, element["@ref"])
                    element["@value"] = param.value.decode("utf-8") 
                   
    def _get_next_row_instance(self, data_subset=None):
        if len(self.table_iterators) > 0 :
            # One table_iterator par TABLE_ROW_TEMPLATE block
            # For now, the case with multiple table_iterator has not been tested
            for key, table_iterator in self.table_iterators.items():
                if data_subset is None or data_subset == key:
                    next_row_instance = table_iterator._get_next_row_instance()
                    if next_row_instance is None:
                        return  None
                    for _, join_iterator in self.join_iterators.items():
                        primary_column = self.column_mapping.get_col_index_by_name(join_iterator.primary_key)
                        join_iterator.set_foreignkey_value(table_iterator.last_row[primary_column])
                        
                        json_block_extractor = JsonBlockExtractor(next_row_instance)
                        json_block_extractor.search_join_container()
                        
                        if len(json_block_extractor.searched_elements) > 0 :
                            json_block_extractor.searched_elements[0][0] = {}
                            cpt = 0
                            inst = None
                            while True:
                                inst = join_iterator.table_mapper._get_next_row_instance()
                                if inst is None:
                                    break
                                elif cpt == 0:
                                    json_block_extractor.searched_elements[0][0] = inst 
                                else:
                                    json_block_extractor.searched_elements[0].append(inst) 
                                cpt += 1

                    return next_row_instance
            raise Exception("cannot find data subset " + data_subset)
        else:
            logger.info("No data table")
            return {}
    
    def _get_next_flatten_row(self, data_subset=None):
        if len(self.table_iterators) > 0 :
            for key, value in self.table_iterators.items():
                if data_subset is None or data_subset == key:
                    return value._get_next_flatten_row()
            raise Exception("cannot find data subset " + str(data_subset))
        else:
            logger.info("No data table")
            return {}

    def resolve_refs_and_values(self, resolve_dmrefs=False):
        root_element = self.table_json
        if resolve_dmrefs is True:
            logger.info("Replace object references with referenced object copies")
            self.resolve_object_references()
        logger.info("Resolve references to PARAMS")
        self._set_header_values(root_element)
        logger.info("Set array iterators")
        self._set_table_iterators(root_element)
        
        logger.info("Resolve mapping leaves")
        self._set_array_subelement_values(self.array, parent_role=None)
        self.map_columns()
     
   
    def map_columns(self):
        logger.info("Map columns")
        self.column_mapping._map_columns(self.parsed_table)
        
    def rewind(self):
        if len(self.table_iterators) > 0 :
            for _, iterator in self.table_iterators.items():
                iterator._rewind()

    def get_flatten_data_head(self, data_subset=None):
        if len(self.table_iterators) > 0 :
            for key, value in self.table_iterators.items():
                if data_subset is None or data_subset == key:
                    return value._get_flatten_data_head()
            raise Exception("cannot find data subset " + str(data_subset))
        else:
            logger.info("No data table")
            return {}
        
    def get_datatable_mapping(self):
        return DictUtils.find_item_by_key(self.table_json, "TABLE_ROW_TEMPLATE")
        
    def get_full_instance(self, resolve_dmrefs=False):
        if resolve_dmrefs is True:
            logger.info("Replace object references with referenced object copies")
            self.resolve_object_references()
        retour = deepcopy(self.table_json[self.table_name])

        json_block_extractor = JsonBlockExtractor(retour)
        json_block_extractor.search_table_row_template_container()
        if len(json_block_extractor.searched_elements) > 0 :
            json_block_extractor.searched_elements[0][0] = {}
            cpt = 0
            inst = None
            while True:
                inst = self._get_next_row_instance()
                if inst is None:
                    break
                elif cpt == 0:
                    json_block_extractor.searched_elements[0][0] = inst 
                else:
                    json_block_extractor.searched_elements[0].append(inst) 
                cpt += 1
        return retour
    
    def get_data_subset_keys(self):
        return self.table_iterators.keys()
           
    def search_instance_by_role(self, searched_role, root_element=None):
        """
        returns a list of element having dmrole = searched_role
        """
        self.searched_elements = []
        if root_element is not None:
            root = root_element
        else:
            root = self.json[Ele.VODML]
            
        json_block_extractor = JsonBlockExtractor(root)
        return json_block_extractor.search_subelement_by_role(searched_role)
    
    def search_instance_by_type(self, searched_type, root_element=None):
        """
        returns a list of element having dmtype = searched_type
        """
        self.searched_elements = []
        if root_element is not None:
            root = root_element
        else:
            root = self.json[Ele.VODML]
            
        json_block_extractor = JsonBlockExtractor(root)
        return json_block_extractor.search_subelement_by_type(searched_type)

 

            
