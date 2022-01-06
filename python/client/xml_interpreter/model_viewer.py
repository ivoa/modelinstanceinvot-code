'''
Created on 5 Jan 2022

@author: laurentmichel
'''
import lxml
from copy import deepcopy
from . import logger
from .exceptions import *
from .annotation_seeker import AnnotatioSeeker
from .resource_seeker import ResourceSeeker
from .table_iterator import TableIterator

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
        self._connected_table_ref = None
        self._current_data_row = None
        self._templates = None
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
        self.connected_table_ref = tableref
        self.connected_table = self._resource_seeker.get_table(tableref)
        if self.connected_table is None:
            raise MappingException("Cannot find table {} in VOTable".format(tableref))
        logger.debug("table %s found in VOTable", tableref)
        
        self._templates = deepcopy(self.annotation_seeker.get_templates_block(tableref))
        if self.top_templates is None:
            raise MappingException("Cannot find TEMPLATES {} ".format(tableref))
        logger.debug("TEMPLATES %s found ", tableref)
        
        self.table_iterator = TableIterator(tableref, self.top_table.to_table())

    
    def get_next_row(self):
        """
        Return the next data row of the connected table 
        """
        self._assert_table_is_connected()
        pass
    
    def rewind(self):
        """
        Rewind the table iterator of the connected table
        """
        self._assert_table_is_connected()
        pass
    
    def get_model_view(self):
        """
        return a XML model view of the last read row
        """
        self._assert_table_is_connected()
        pass
    
    def get_json_model_view(self):
        """
        return a JSON model view of the last read row
        """
        self._assert_table_is_connected()
        pass
    
    def get_json_model_component_by_type(self, dmtype):
        """
        return the first instance with dmtype=dmtype from the json view of the current data row
        Return a {} if no matching dmtype is found 
        """
        self._assert_table_is_connected()
        pass
    
    def get_json_model_component_by_role(self, dmrole):
        """
        return the first instance with dmrole=dmrole from the json view of the current data row
        Return a {} if no matching dmrole is found 
        """
        self._assert_table_is_connected()
        pass
    
    """
    Private methods
    """
    def _assert_table_is_connected(self):
        assert self._connected_table is not None, "Operation failed: no connected data table"
        
    def _assert_resource_is_result(self):
        print(self._resource.type)
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
            self._annotation_seeker = AnnotationSeeker(lxml.etree.fromstring(content))

        logger.info("VODML found")

