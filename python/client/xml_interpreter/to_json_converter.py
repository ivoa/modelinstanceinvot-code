'''
Created on 21 Dec 2021

@author: laurentmichel
'''
import lxml
import xmltodict
from numpy import float64

from client.xml_interpreter.json_block_extractor import JsonBlockExtractor
from utils.dict_utils import DictUtils

class ToJsonConverter(object):
    '''
    classdocs
    '''
    def __init__(self, xml_instance):
        '''
        Constructor
        Xml_instance with a `<TEMPLATES tablefref=tablename..>` node
        :param xml_instance: XML view of the instance
        :type  xml_instance: etree
        '''
        self.xml_instance = xml_instance
        self.json_instance = None
        
    def _translate_xml(self):
        '''
        Translates the xml block given to the constructor into a 
        dictionary with the following structure:
        { tablename:[{obj1}, .... {objn}] where {obj1}, .... {objn} are the objects mapping one table row.
        These are actually made with the content of dmrole-less INSTANCE elements.
        The INSTANCE keys are removed to hide these objects to the further processing which would fail
        due to the lack ofdmrole.
        '''
        xmv = lxml.etree.tostring(self.xml_instance)
        tmp_json_block = xmltodict.parse(xmv) 
        tmp_json_block_tmpl = tmp_json_block["TEMPLATES"]
        self.json_instance = {}
        self.json_instance[tmp_json_block_tmpl["@tableref"]] = []
        tbl = self.json_instance[tmp_json_block_tmpl["@tableref"]]
        for key, value in tmp_json_block_tmpl.items():
            if key.startswith("@") is True:
                continue
            tbl.append(value)
                 
    def _revert_collections(self):
        '''
        Replaces the COLLECTION keys with the roles they are affected to
        "COLLECTION: { @dmrole:role, key1: {obj1} ... keyn: {objn}}
        => role: [{obj1},.... {objn}]
        It is to be noted that the collection items have no individual roles, 
        this why they can be stacked in a list
        See JsonBlockExtractor to see how the recursive processing does work
        '''
        revert_coll = JsonBlockExtractor.search_array_container(self.json_instance, "COLLECTION")
        for item in revert_coll:
            host = item["host"]
            content = item["content"]
            host[content["@dmrole"]]  = [] 
            coll_mapping = host[content["@dmrole"]]
            for key, value in content.items():
                if key != '@dmrole':
                    if isinstance(value, list):
                        for li in value:
                            coll_mapping.append(li)

            host.pop(item["key"])
            
    def _revert_attributes(self):
        '''
        Replaces the ATTRIBUTE keys with the roles they are affected to
        Standalone attribute are translated that way:
        ATTRIBUTE:{role, type, value, ref} => role: value
        At this level (json translation) the mapping is assumed to be complete this why we just keep the value.
        The types are used to set the value (strings in XML) with the correct format.
        If the ATTRIBUTE container contains an attribute sequence, xmltojson issues a list.
        In this case, the method bui a key/value sequence
        ATTRIBUTE:[ {att1}... {attn}] ==> role1: val1, .... rolen:valn   
        See JsonBlockExtractor to see how the recursive processing does work
        '''
        attr_list = JsonBlockExtractor.search_object_container(self.json_instance, "ATTRIBUTE")
        for attr in attr_list:
            content = attr["content"]
            host = attr["host"]
            # A sequence of attributes is translated as a ATTRIBUTE[]
            if isinstance(content, list) is True:
                for att_item in content:
                    role = att_item["@dmrole"]
                    host[role] = att_item
                    host[role].pop("@dmrole")
                    self._restore_attribute_type(att_item)
                    # Set role=value can be disabled for debug
                    host[role] = att_item["@value"]
            else:
                role = content["@dmrole"]
                host[role] = content
                host[role].pop("@dmrole")
                self._restore_attribute_type(content)
                # Set role=value can be disabled for debug
                host[role] = content["@value"]
            host.pop(attr["key"])

    
    def _restore_attribute_type(self, attr):
        '''
        Format the attribute value according to the dmtype
        :param attr: attribute node: {role, type, value, ref}
        '''
        
        atype = attr["@dmtype"]
        avalue = attr["@value"]
        if atype == "ivoa:boolean":
            attr["@value"] = bool(avalue)
        elif atype == "ivoa:integer":
            attr["@value"] = int(avalue)
        elif atype == "ivoa:RealQuantity" or atype == "ivoa:real":
            attr["@value"] = float64(avalue)
            
    def _revert_instances(self):
        '''
        Replaces the INSTANCE keys with the roles they are affected to
        Standalone instances are translated that way:
        ATTRIBUTE:{role, type, key:value... key:value} => role: {type, key:value... key:value}
        If the INSTANCE container contains an instance sequence, xmltojson issues a list.
        In this case, the method buit a role:{}  sequence
        INSTANCE:[ {inst1}... {instn}] ==> role1: {inst1}, .... rolen:{instn}   
        See JsonBlockExtractor to see how the recursive processing does work
        '''
        attr_list = JsonBlockExtractor.search_object_container(self.json_instance, "INSTANCE")
        for attr in attr_list:
            content = attr["content"]
            host = attr["host"]
            if isinstance(content, dict):
                if "@dmrole" not in content:
                    DictUtils.print_pretty_json(attr)
                role = content["@dmrole"]
                host[role] = content
                host[role].pop("@dmrole")
            else:
                for item in content:
                    host[item["@dmrole"]] = item
                    item.pop("@dmrole")
            host.pop(attr["key"])

    
    def get_json_instance(self):
        '''
        Run the sequence of operations that will issue a clean serialization if the object
        The result is a list of instances role-less.
        '''
        self._translate_xml()
        self._revert_collections()
        self._revert_attributes()
        self._revert_instances()
        # just take the content of the key matching the table name
        # The conversion returns  { "Results": [...]}
        # we want [...] which is the templates content
        for _, value in self.json_instance.items():
            return value
        return self.json_instance

