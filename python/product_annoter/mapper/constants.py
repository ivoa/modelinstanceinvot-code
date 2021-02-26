'''
Created on 15 avr. 2020

@author: laurentmichel
'''
from collections import namedtuple

ParamTemplates = namedtuple('ParamTemplates', ['POSITION'])
PARAM_TABLE_MAPPING = ParamTemplates(
    """
    <INSTANCE dmrole="mango:MangoObject.parameters" dmtype="mango:Parameter">
    <ATTRIBUTE dmrole="mango:Parameter.semantic" dmtype="ivoa:string" value="@@@@@@"/>
    <ATTRIBUTE dmrole="mango:Parameter.ucd" dmtype="ivoa:string" value="@@@@@@"/>
    <ATTRIBUTE dmrole="mango:Parameter.description" dmtype="ivoa:string" value="@@@@@@"/>
    </INSTANCE>
    """
    )

AttributeDefault = namedtuple('AttributeDefault', ['TO_BE_SET', 'NOT_SET'])
ATTRIBUTE_DEFAULT = AttributeDefault(
    "@@@@@@",
    "NotSet"
    )
