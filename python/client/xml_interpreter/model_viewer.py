'''
Created on 5 Jan 2022

@author: laurentmichel
'''

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

    def __init__(self, resource):
        '''
        Constructor
        :param resource: VOTable resource
        :type resource: astropy.Resource
        '''
        self._resource = resource
        self._mapping_block_seeker = None
        self._resource_seeker = None
        self._connected_table = None
        self._current_data_row = None
    
    """
    Properties
    """
    @property
    def mapping_block_seeker(self):
        return self._mapping_block_seeker
    
    @property
    def resource_seeker(self):
        return self._resource_seeker
    
    @property
    def connected_table(self):
        return self._connected_table
    
    @property
    def current_data_row(self):
        return self._current_data_row
    
    """
    Global accessors
    """
    def get_resource_seeker(self):
        """
        Return an API to search various components in self._resource
        """
        pass
    
    def get_mapping_block_seeker(self):
        """
        Return an API to search various components in the XML mapping block
        """
        pass
    
    def get_table_ids(self):
        """
        return a list of the table located just below self.resource
        """ 
        pass
    
        
    def get_globals_models(self):
        """
        :return : The dmtypes of all the top level INSTANCE/COLLECTION of GLOBALS
        :rtype:  {'COLLECTIONS': [dmtpyes], 'INSTANCE': [dmtypes]}
        """
        pass
    
    def get_templates_models(self):        
        """
        :return : The dmtypes (except ivoa:*) of all INSTANCE/COLLECTION of all TEMPLATES
        :rtype:  {'tableref: {'COLLECTIONS': [dmtpyes], 'INSTANCE': [dmtypes]}, ...}
        """
        pass
    
    """
    Data browsing
    """
    def get_globals_instance(self, dmtype):
        """
        The a model view on the GLOBALS object (INSTANCE or COLLECTION) with dmtype as dmtype
        """
        pass
    
    def connect_table(self, table_ref):
        """
        Iterate over the table identified by tableref
        Required to browse table data
        """
        pass
    
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
        assert(self._connected_table is not None, "Operation failed: no connected data table")

    
