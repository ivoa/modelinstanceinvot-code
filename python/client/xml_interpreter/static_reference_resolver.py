'''
Created on 22 Dec 2021

@author: laurentmichel
'''
from copy import deepcopy
from client.xml_interpreter.exceptions import MappingException

class StaticReferenceResolver(object):
    '''
    Namespace for the  function processing the static REFERENCEs
    '''

    @staticmethod 
    def resolve(annotation_seeker, templates_ref, instance):
        '''
        Resolve all static REFERENCEs found in instance.
        The referenced objects are first searched in GLOBALS and then
        in the templates_ref table.
        REFERENCE elements are replaced with the referenced objects set with the roles of the REFERENCEs
        - A exception is risen if the reference cannot be resolved
        - Works even if REFERENCE tags are numbered by the former processing
        :param templates_ref: Identifier of the table where instance comes from
        :param instance: etree Element
        '''
        for ele in instance.xpath(".//*[starts-with(name(), 'REFERENCE_')]"):
            dmref = ele.get("dmref")
            if dmref == None:
                return
            target = annotation_seeker.get_globals_instance_by_dmid(dmref)
            found_in_global = True
            if target is None and templates_ref is not None:
                target = annotation_seeker.get_templates_instance_by_dmid(templates_ref, dmref)
                found_in_global = False
            if target is None:
                raise MappingException("Cannot resolve reference={}".format(dmref))
            # Resolve static references recursively
            if found_in_global is False:
                StaticReferenceResolver.resolve(annotation_seeker, templates_ref, ele)
            else:
                StaticReferenceResolver.resolve(annotation_seeker, None, ele)
            # Set the reference role to the copied instance
            target_copy = deepcopy(target)
            target_copy.attrib["dmrole"] = ele.get('dmrole')
            # Insert the referenced object
            ele.getparent().append(target_copy)
            # Drop the reference
            ele.getparent().remove(ele)
            

