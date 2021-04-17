'''
Created on 1 avr. 2020

@author: laurentmichel
'''
from collections import OrderedDict

class ColumnMapping():
    '''
    This class manages the kind between the table columns and the mapping element (ARRAY---> ATTRIBUTE)  
    The column reference entries must be set (self.add_entry) before to build the column dictionary (column_ids)
    The latest is created at the same time the reference are resolved (self._map_columns)
    Watchout: The case where more the 1 mapping element point on the same column hasn't been tested,
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Dictionary of the columns (or fields) referenced by the mapping
        # key: {parent_role, role, index (= col number), field (= col id)} 
        # This attribute contains the mapping
        self.column_refs = OrderedDict()
        # Dictionary of the VOTable fields 
        # key: {name, ref, id}
        #   key is then field position (starting from 0)
        #   name and id are FIELD attribute
        #   ref is the  field identifier used by the mapping element 
        #   (@ref attribute) that uses the column
        # This attribute is just used facilitate the mapping setup and to 
        # keep a convenient representation of the table fields 
        self.column_ids = OrderedDict()
       
    def __repr__(self):
        """
        string representation
        """
        return "column_refs:{} \n column_ids:{}".format(
            self.column_refs,
            self.column_ids)
    
    def add_entry(self, key, role, parent_role=None, parent_type=None):
        """
        Add an entry to the dictionary of the referenced columns
        The new is created without reference to the VOtable fields
        The cross references VOTable fields and columns used by he mapping are resolved later.
        
        :param key: field identifier used by the mapping (@ref attribute)
        :type key: string
        :param role: Role of the attribute referring to the columns (@dmrole attribute)
        :type role: string
        :param parent_role: Role of the parent instance of the attribute 
                            referring to the columns (@dmrole attribute)
        :type parent_role: string
        :param parent_type: Type of the parent instance of the attribute 
                            referring to the columns (@dmtype attribute)
        :type parent_type: string
        """
        if key not in self.column_refs.keys():
            self.column_refs[key] = {
                "parent_role": parent_role,
                "parent_type": parent_type,
                "role": role,
                "index": None,
                "field": None,
                "ucd": None
                }
      
    def _map_columns(self, votable):
        """
        links column references with column ids.
        Links are set with both "index" and "field" attribute of column references objects
        TODO The case of un-mapped column reference must be clarified
        :param votable: Parsed votable.table
        :type votable: astropy.io.votable.table  
        """        
        keys = self.keys()
        # Look first for params possibly matching the column references 
        indx = -1
        for param in  votable.params:
            if param.ID in keys :
                self.set_value(param.ID, indx, param)
            elif param.ref in keys :
                self.set_value(param.ref, indx, param)
            elif param.name in keys :
                self.set_value(param.name, indx, param)

        indx = 0      
        # The we try we FIELD so that FIELD can override PARAMs links
        for field in  votable.fields:
            self.column_ids[indx] = {
                "name": field.name,
                "ref": field.ref,
                "id": field.ID,
                "ucd": field.ucd
                }
            if field.ID in keys :
                self.set_value(field.ID, indx, field, field.ucd)
            elif field.ref in keys :
                self.set_value(field.ref, indx, field, field.ucd)
            elif field.name in keys:
                self.set_value(field.name, indx, field, field.ucd)
            indx += 1
        
    def set_value(self, key, index, field_or_param, ucd):
        """
        Connect the column reference identified by 'key' with the FIELD or the PARAMS
        pointed by "field_or_param"
        :param key: Field identifier. can be an ID, a name or a  ref
        :type key: string
        :param index: column index (starts with 0)
        :type index: integer
        :param field_or_param:
        :type field_or_param: astropy.votable field or param
        :param ucd:
        :type ucd: string
        """
        # for the record: does nothing if the entry already exists
        self.add_entry(key, None)
        self.column_refs[key]["index"] = index
        self.column_refs[key]["field"] = field_or_param
        self.column_refs[key]["ucd"] = ucd

    def get_col_index_by_name(self, name):        
        """
        :param name: name or ID of the columns of the search index
        :type name: string
        :return: the index  of the column reference named as "name"
        :rtype : dictionary {parent_role, role, index, field}
        """
        for k, v in self.column_ids.items():
            if "id" in v.keys() and v["id"] == name:
                return k   
        for k, v in self.column_ids.items():
            if "name" in v.keys() and v["name"] == name:
                return k   
        return None

    def get_index(self, key):
        """
        an exception is risen if the column reference does not exist
        :return: the index of the column reference (column_refs[key]) identified by "key"
        :rtype : integer
        """
        return self.column_refs[key]["index"]  
    
    def get_mapping_index(self, key):
        """
        :return: the index of the mapped column identified by "key"
        :rtype : integer
        """
        cpt = 0;
        for cr_key, _ in self.column_refs.items():
            if cr_key == key:
                return cpt
            cpt += 1
        return None
  
    
    def get_field_or_param(self, key):
        """
        an exception is risen if the column reference does not exist
        :return: the field or the param attached to the column reference (column_refs[key]) identified by "key"
        :rtype : integer
        """
        return self.column_refs[key]["field"]
    
    def get_key(self, index):
        """
        :param index: index of the search column reference
        :type index: integer
        :return: the identifier of the column reference connected with the FILD having the position "index:
        :rtype: string
        """
        for k, v in self.column_refs:
            if v["index"] == index:
                return k
        return None
    
    def get_indexes(self):
        """
        :return: list of the indices of all mapped column
        :rtype: list of strings
        """
        retour = []
        for _, v in self.column_refs.items():
            retour.append(v["index"])
        return retour
    
    def get_column_head(self):
        """
        human readable description of the column mapping allow to see which model quantity (column reference)
        is connected with which VOTable Field
        :return: textual description of the column mapping
        :rtype: string
        """
        retour = []
        for key, v in self.column_refs.items():
            if v["role"].startswith("ivoa:") is True:
                str_role = ""
            else :
                str_role = "->{}".format(v["role"])

            retour.append("{} ({}{}) [col#{} {} ({})]". format(v["parent_type"], v["parent_role"], str_role, v["index"], key, v["ucd"]))
        return retour
    
    def keys(self):
        """
        :return: list of all column reference identifiers
        :rtype: list of strings
        """
        return list(self.column_refs.keys())
    
    def get_index_from_field(self, field):
        """
        Returns the rank of the FIELD having either id or name == field
        :param field: name or ID of the searched field
        :tyhpe field: string
        :return : column index of the searches field
        :rtype: int
        """
        for index, column_id in self.column_ids.items():
            if column_id["id"] == field or column_id["name"] == field:
                return index
        return None
