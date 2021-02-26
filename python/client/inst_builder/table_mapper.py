'''
Created on 31 mars 2020

@author: laurentmichel
'''
import json
from astropy.io.votable import parse_single_table  
from client.inst_builder.column_mapping import ColumnMapping
from client.inst_builder.table_iterator import TableIterator
from client.inst_builder.join_iterator import JoinIterator
from client.inst_builder.row_filter import RowFilter
from client.inst_builder import logger, json_block_extractor
from client.inst_builder.json_block_extractor import JsonBlockExtractor
from client.inst_builder.att_utils import AttUtils

from copy import deepcopy
from client.inst_builder.groupby_processor import GroupByProcessor
from utils.dict_utils import DictUtils


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
        
        # array block reference 
        self.array = None
        # key = role of the instance contained TABLE_ROW_TEMPLATE value = TableIterator
        self.table_iterators = {}
        self.column_mapping = ColumnMapping()
        # key = foreign table name value = TableIterator
        self.join_iterators = {}
        self.join = None
        # replace groupby with a suite of collection (one for each different key value
        self._process_groupby()
        
    def _process_groupby(self):
        """
        Replace the GROUPBY block with a sequence of collections, filtering each one one group value
        The dmrole of these generated collections is string representation of the group value 
        The dmrole of the collection enclosed in each virtual collection is the concatenation 
        of the original role with the group value. This is requested to avoid duplicated keys in the table iterators
        """
        if "GROUPBY" in self.json['MODEL_INSTANCE']['TABLE_MAPPING'][self.table_name].keys():
            gbkey = self.json['MODEL_INSTANCE']['TABLE_MAPPING'][self.table_name]["GROUPBY"]["@ref"]
            groupby_processor = GroupByProcessor(self.table_name,
                                                 gbkey,
                                                 self.json['MODEL_INSTANCE']['TABLE_MAPPING'][self.table_name],
                                                 self.table)
            ungrouped_mapping_block = groupby_processor.build_group_mapping()
            for key in ungrouped_mapping_block.keys():
                logger.info("add a virtual collection with dmrole=%s", key)
                self.json['MODEL_INSTANCE']['TABLE_MAPPING'][self.table_name][key] = ungrouped_mapping_block[key]
            self.json['MODEL_INSTANCE']['TABLE_MAPPING'][self.table_name].pop("GROUPBY")
        
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

    def _set_array_iterators(self, root_element):
        """
        Build and array iterator for each TABLE_ROW_TEMPLATE element found within root_element
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                if self.retour is None:
                    self._set_array_iterators(root_element[idx])
        elif isinstance(root_element, dict):
            for k, v in root_element.items():
                if k == 'TABLE_ROW_TEMPLATE':
                    self.array = v 
                    row_filter = None
                    iterator_key = None
                    for ro in self.array.keys():
                        if ro == 'FILTER' :
                            row_filter = RowFilter(self.array['FILTER'])
                            iterator_key = row_filter.name
                            logger.info("Add filter %s", row_filter.name)
                        else:
                            iterator_key = ro
                            logger.info("Set table iterator for object with role=%s", ro)
                            self.table_iterators[ro] = TableIterator(
                                iterator_key,
                                self.parsed_table.to_table(),
                                self.array[ro],
                                self.column_mapping,
                                row_filter=row_filter
                                )
                    pass
                elif k == 'JOIN':
                    self.join = v 
                    iterator_key = self.join["@tableref"]
                    logger.info("Set join iterator with table=%s", iterator_key)
                    for ro in self.join.keys():
                        self.join_iterators[iterator_key] = JoinIterator(
                            iterator_key,
                            self.join["@primary"],
                            self.join["@foreign"],
                            self.join
                            )
                        # JOIN has only one child
                        break
                    pass
                
                if isinstance(v, list):
                    for ele in v:
                        self._set_array_iterators(ele)
                elif isinstance(v, dict):  
                    # self._set_value(v)
                    self._set_array_iterators(v)

    def _set_array_subelement_values(self, array_element, parent_role=None):
        """
        Recursive function
        Takes all @ref of the array_element content and map them the table columns
        """
        if isinstance(array_element, list):
            for idx, _ in enumerate(array_element):
                if self.retour is None:
                    self._set_array_subelement_values(array_element[idx])
        elif isinstance(array_element, dict):
            for k, v in array_element.items():
                # Join content refers to others tables, 
                # it is processed the the join_iterator 
                if k == "JOIN":
                    return
                if isinstance(v, list):
                    for ele in v:
                        self._set_array_subelement_values(ele)
                elif isinstance(v, dict): 
                    self._set_value(v, role=k, parent_role=parent_role)
                    self._set_array_subelement_values(v, parent_role=k)
                         
    def _get_object_references(self, root_element, replacement_list):
        """
        recursive function
        Looks into root_element for element being references (INSTANCE with @dmref)
        Objects found are stored in replacement_list
        
        :param root_element: Root element for the search
        :type root_element: XML element
        :param replacement_list: List of the found elements
        :type replacement_list: list of {"node": element found, "key": role if thye reference, "dmref": instance reference}
        """
        if isinstance(root_element, list):
            for idx, _ in enumerate(root_element):
                self._get_object_references(root_element[idx], replacement_list)
        elif isinstance(root_element, dict):
            if AttUtils.is_object_ref(root_element):
                pass
            for k , v in root_element.items():
                if isinstance(v, list):
                    for ele in v:
                        self._get_object_references(ele, replacement_list)
                elif isinstance(v, dict):  
                    if AttUtils.is_object_ref(v):
                        replacement_list.append(
                            {"node": root_element,
                             "key": k,
                             "dmref": v["@dmref"]})
                        return replacement_list
                        # self.searched_types.append(v)
                    self._get_object_references(v, replacement_list)
        return []            
    
    def _set_value(self, element, role=None, parent_role=None):
        """
        Create a column mapping entry for the element if it is a @ref
        both role an parent_role are just labels used make more explicit 
        the string representation of the columns mapping
        """
        keys = element.keys()
        if ("@dmtype" in keys and "@ref" in keys 
            and "@value" in keys and element["@value"] == ""):  
            logger.info("Give role %s to the column %s "
                        , parent_role, element["@ref"])
            self.column_mapping.add_entry(element["@ref"], role, parent_role)
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

    def resolve_refs_and_values(self, resolve_refs=False):
        root_element = self.json['MODEL_INSTANCE']['TABLE_MAPPING'][self.table_name]
        if resolve_refs is True:
            logger.info("Replace object references with referenced object copies")
            self.resolve_object_references()
        logger.info("Resolve references to PARAMS")
        self._set_header_values(root_element)
        logger.info("Set array iterators")
        self._set_array_iterators(root_element)
        logger.info("Resolve mapping leaves is an TABLE_ROW_TEMPLATE block")
        self._set_array_subelement_values(self.array, parent_role=None)
        
    def map_columns(self):
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
        
    def get_full_instance(self, resolve_refs=False):
        if resolve_refs is True:
            logger.info("Replace object references with referenced object copies")
            self.resolve_object_references()
        retour = deepcopy(self.json['MODEL_INSTANCE']['TABLE_MAPPING'][self.table_name])

        json_block_extractor = JsonBlockExtractor(retour)
        json_block_extractor.search_array_container()
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
            root = self.json['MODEL_INSTANCE']
            
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
            root = self.json['MODEL_INSTANCE']
            
        json_block_extractor = JsonBlockExtractor(root)
        return json_block_extractor.search_subelement_by_type(searched_type)

    def resolve_object_references(self):
        #
        # resolve object reference
        # an object reference is something like {"@ref"=xxx}
        # Refrences are replaced with copies of object looking like
        #  {"@ID"=xxx ...}
        #
        root = self.json
        while True:
            replacement_list = []  

            self._get_object_references(root, replacement_list)
            if len(replacement_list) == 0:
                break
            else :
                for replacement in replacement_list:
                    instance = self.search_instance_by_id(replacement["dmref"], root)[0]
                    replacement["node"][replacement["key"]] = deepcopy(instance)
     
    def search_instance_by_id(self, searched_id, root_element=None):
        self.searched_ids = []
        if root_element is not None:
            root = root_element
        else:
            root = self.json['MODEL_INSTANCE']
        json_block_extractor = JsonBlockExtractor(root)
        return json_block_extractor.search_subelement_by_id(searched_id)

            
