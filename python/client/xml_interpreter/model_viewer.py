'''
Created on 5 Jan 2022

@author: laurentmichel
'''
from lxml import etree
from copy import deepcopy
from . import logger
from .exceptions import *
from .annotation_seeker import AnnotationSeeker
from .resource_seeker import ResourceSeeker
from .table_iterator import TableIterator
from .static_reference_resolver import StaticReferenceResolver
from .dynamic_reference import DynamicReference
from .to_json_converter import ToJsonConverter
from .json_block_extractor import JsonBlockExtractor
from .join_operator import JoinOperator
from client.stc_classes.measure import Measure
from client.stc_classes.measure import Position, Time, GenericMeasure
from client.astropy_wrapper.sky_coord import SkyCoord

from utils.dict_utils import DictUtils
class ModelViewer(object):
    '''
    ModelViewer is a PyVO table wrapper aiming at providing a model view on VOTable data read with usual tools
    
    Standard usage applied to data rows
    
    .. code-block:: python
        votable = parse(votable_path)
        for resource in votable.resources:
            model_viewer = ModelViewer(resource)
            model_viewer.connect_table("results")
            while True:
                data_row = model_viewer.get_next_row()
                if data_row is None:
                    break
                model_view = model_viewer.get_model_view()
                json_model_view = model_viewer.get_json_model_view()
            break

    Standard usage applied to global instances

    .. code-block:: python
        votable = parse(votable_path)
        for resource in votable.resources:
            model_viewer = ModelViewer(resource)
            time_series = model_viewer.get_globals_instance("cube:TimeSeries")      

    '''

    def __init__(self, resource, votable_path=None):
        '''
        Constructor
        votable_path is a workaround allowing to extract the annotation block outside of astropy
        :param resource: VOTable resource
        :type resource: astropy.Resource
        '''
        self._resource = resource
        self._assert_resource_is_result()
        self._annotation_seeker = None
        self._resource_seeker = ResourceSeeker(self._resource)
        self._connected_table = None
        self._connected_tableref = None
        self._current_data_row = None
        self._last_row=None
        self._templates = None
        self._joins = {}
        self._dyn_references = {}
        self._extract_mapping_block(votable_path=votable_path)
    
    """
    Properties
    """
    @property
    def annotation_seeker(self):
        """
        Return an API to search various components in the XML mapping block
        """
        return self._annotation_seeker
    
    @property
    def resource_seeker(self):
        """
        Return an API to search various components in the VOTabel resource
        """
        return self._resource_seeker
    
    @property
    def connected_table(self):
        return self._connected_table
    
    @property
    def connected_table_ref(self):
        return self._connected_table_ref
    
    @property
    def current_data_row(self):
        self._assert_table_is_connected()
        return self._current_data_row
    
    """
    Global accessors
    """    
    def get_table_ids(self):
        """
        return a list of the table located just below self.resource
        """ 
        return self.resource_seeker.get_table_ids()
    
        
    def get_globals_models(self):
        """
        Collection types are GLOBALS/COLLECTION/INSTANCE@dmtype: used for collections of static objects
        :return : The dmtypes of all the top level INSTANCE/COLLECTION of GLOBALS
        :rtype:  {'COLLECTION': [dmtpyes], 'INSTANCE': [dmtypes]}
        """
        retour = {}
        retour["COLLECTION"] = self._annotation_seeker.get_globals_collection_dmtypes()
        retour["INSTANCE"] = self._annotation_seeker.get_globals_instance_dmtypes()
        return retour
    
    def get_templates_models(self):        
        """
        COLLECTION not implemented yet
        :return : The dmtypes (except ivoa:*) of all INSTANCE/COLLECTION of all TEMPLATES
        :rtype:  {'tableref: {'COLLECTIONS': [dmtpyes], 'INSTANCE': [dmtypes]}, ...}
        """
        retour = {}
        gni = self._annotation_seeker.get_instance_dmtypes()['TEMPLATES']
        for tid, tmplids in gni.items():
            retour[tid] = {'COLLECTIONS':[], 'INSTANCE':tmplids}
        
        return retour
    
    """
    Data browsing
    """
    def get_globals_instance(self, dmtype):
        """
        The a model view on the GLOBALS object (INSTANCE or COLLECTION) with @dmtype=dmtype
        """
        raise NotImplementedException("GLOBALS Instance access not implemented")
    
    def connect_table(self, tableref):
        """
        Iterate over the table identified by tableref
        Required to browse table data.
        Connect to the first table if tableref is None
        """
        self._connected_tableref = tableref
        self._connected_table = self._resource_seeker.get_table(tableref)
        if self.connected_table is None:
            raise MappingException("Cannot find table {} in VOTable".format(tableref))
        logger.debug("table %s found in VOTable", tableref)
        
        self._templates = deepcopy(self.annotation_seeker.get_templates_block(tableref))
        if self._templates is None:
            raise MappingException("Cannot find TEMPLATES {} ".format(tableref))
        logger.debug("TEMPLATES %s found ", tableref)
        
        self.table_iterator = TableIterator(tableref, self.connected_table.to_table())
        self._squash_join_and_references()
        self._set_column_indices()
    
    def get_next_row(self):
        """
        Return the next data row of the connected table 
        """
        self._assert_table_is_connected()
        self._current_data_row = self.table_iterator._get_next_row()
        return self._current_data_row
    
    def rewind(self):
        """
        Rewind the table iterator of the connected table
        """
        self._assert_table_is_connected()
        self.table_iterator._rewind()
    
    def get_model_view(self, resolve_ref=True):
        """
        return a XML model view of the last read row
        """
        self._assert_table_is_connected()
        
        templates_copy = deepcopy(self._templates)
        if resolve_ref is True:
            StaticReferenceResolver.resolve(self._annotation_seeker, self._connected_tableref, templates_copy)
        for ele in templates_copy.xpath("//ATTRIBUTE"):
            ref = ele.get("ref")
            if ref is not None:
                index = ele.attrib["index"]
                ele.attrib["value"] = str(self._current_data_row[int(index)])
        for dref_tag, dref in self._dyn_references.items():
            logger.info("resolve reference %s", dref_tag)
            dyn_resolver = DynamicReference(self, dref_tag, self._connected_tableref, dref)
            dyn_resolver._set_mode()
            ref_target = dyn_resolver.get_target_instance(self._current_data_row)
            ref_element = templates_copy.xpath("//" + dref_tag)[0]
            ref_host = ref_element.getparent()
            ref_target_copy = deepcopy(ref_target)
            # Set the reference role to the copied instance
            ref_target_copy.attrib["dmrole"] = ref_element.get('dmrole')
            # Insert the referenced object
            ref_host.append(ref_target_copy)
            # Drop the reference
            ref_host.remove(ref_element)
            
        for join_tag, join in self._joins.items():
            logger.info("resolve join %s", join_tag)
            join_operator = JoinOperator(self, self._connected_tableref, join)
            join_operator._set_filter()
            join_operator._set_foreign_instance()
            join_operator.get_matching_data(self._current_data_row)
            ref_element = templates_copy.xpath("//" + join_tag)[0]
            ref_host = ref_element.getparent()
            for cpart in join_operator.get_matching_model_view(resolve_ref=resolve_ref):          
                ref_host.append(deepcopy(cpart))
            # Drop the reference
            ref_host.remove(ref_element)



        return templates_copy

    def get_json_model_view(self, resolve_ref=True):
        """
        return a JSON model view of the last read row
        """
        self._assert_table_is_connected()
        logger.debug("build json view")
        tjc = ToJsonConverter(self.get_model_view(resolve_ref=resolve_ref))
        return tjc.get_json_instance()

    
    def get_json_model_component_by_type(self, searched_dmtype):
        """
        return the first instance with @dmtype=searched_ from the json view of the current data row
        Return a {} if no matching dmtype was found 
        """
        self._assert_table_is_connected()
        json_view = self.get_json_model_view()
        return JsonBlockExtractor.search_subelement_by_type(json_view, searched_dmtype)

    def get_model_component_by_type(self, searched_dmtype):
        """
        return the list of the xml instances with @dmtype=searched_ type from the model view of the current data row
        Return a {} if no matching dmtype was found 
        """
        self._assert_table_is_connected()
        retour = []
        model_view = self.get_model_view(resolve_ref=True)
        for ele in model_view.xpath(f'.//INSTANCE[@dmtype="{searched_dmtype}"]'):
            retour.append(deepcopy(ele)) 
        return retour
    
    def get_json_model_component_by_role(self, searched_dmrole):
        """
        return the first instance with dmrole=dmrole from the json view of the current data row
        Return a {} if no matching dmrole is found 
        """
        self._assert_table_is_connected()
        json_view = self.get_json_model_view()
        return JsonBlockExtractor.search_subelement_by_role(json_view, searched_dmrole)

    def get_stc_positions(self):
        """
        returns the all positions found as a list of STC Positions instances  
        """
        retour = []
        for position in self.get_model_component_by_type("meas:Position"):
            retour.append(Position(position))
        return retour
    
    def get_stc_times(self):
        """
        returns the all time measure found as a list of STC Time instances  
        """
        retour = []
        for time in self.get_model_component_by_type("meas:Time"):
            retour.append(Time(time))
        return retour
    
    def get_stc_generic_measures(self):
        """
        returns the all generic measures found as a list of STC Time instances  
        """
        retour = []
        for measure in self.get_model_component_by_type("meas:GenericMeasure"):
            retour.append(GenericMeasure(measure))
        return retour
    
    def get_stc_measures(self):
        """
        returns the all measures found as a list of STC Positions instances  
        """
        retour = []
        model_view = self.get_model_view(resolve_ref=True)
        for ele in model_view.xpath(f'.//INSTANCE[ATTRIBUTE[@dmrole="meas:Measure.ucd"]]'):
            retour.append(Measure.get_measure(ele)) 
        return retour

    def get_stc_measures_by_ucd(self, ucd):
        """
        returns the all measures found as a list of STC Positions instances  
        """
        retour = []
        model_view = self.get_model_view(resolve_ref=True)
        for ele in model_view.xpath(f'.//INSTANCE[ATTRIBUTE[@dmrole="meas:Measure.ucd" and @value="{ucd}"]]'):
            retour.append(Measure.get_measure(ele)) 
        return retour

    def get_astropy_sky_coord(self):
        """
        Returns an instance of Astropy.SkyCoord if the set of mapped STC Measures allows it.
        None otherwise
        """
        return SkyCoord(self.get_stc_measures()).get_sky_coord()
        

    
    """
    Private methods
    """
    def _assert_table_is_connected(self):
        assert self._connected_table is not None, "Operation failed: no connected data table"
        
    def _assert_resource_is_result(self):
        assert self._resource.type == "results", "ModelViewer must be set on a Resource with type=results"

    def _extract_mapping_block(self, votable_path=None):
        """
        String extraction must be replaced with astropy.Resource.model_mapping when available
        """
        logger.info("extract vodml block from %s", votable_path)
        with open(votable_path) as xml_file:
            content = xml_file.read()
            start = content.index('<dm-mapping:VODML')
            if start == -1:
                raise MappingException("Cannot find mapping block")
            content = content[start:]
            stop_pattern = '</dm-mapping:VODML>'
            stop = content.index(stop_pattern) + len(stop_pattern)
            content = content[:stop]
            self._annotation_seeker = AnnotationSeeker(etree.fromstring(content))

        logger.info("VODML found")

    def _squash_join_and_references(self):
        """
        Remove both JOINs and REFERENCEs fron the templates and store them in to be resolved later on
        This avoid to have the model view polluted with elements that are not in the model
        """
        for ele in self._templates.xpath("//*[starts-with(name(), 'REFERENCE_')]"):
            if ele.get("tableref") is not None:
                self._dyn_references = {ele.tag: deepcopy(ele)}
                for child in list(ele):
                    ele.remove(child)
        
        for ele in self._templates.xpath("//*[starts-with(name(), 'JOIN')]"):
            self._joins = {ele.tag: deepcopy(ele)}
            for child in list(ele):
                ele.remove(child)    

    def _set_column_indices(self):
        """
        add column ranks to attribute having a ref.
        Using ranks allow to identify columns even numpy raw have been serialised as []
        """
        index_map = self._resource_seeker.get_id_index_mapping(self._connected_tableref)
        for ele in self._templates.xpath("//ATTRIBUTE"):
            ref = ele.get("ref")
            if ref is not None:
                ele.attrib["index"] = str(index_map[ref])
                