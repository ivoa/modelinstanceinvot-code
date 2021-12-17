'''
Created on 30 août 2021

author: michel
'''

class Ele(object):
    '''
    classdocs
    '''
    namespace = ""
    VODML = namespace + "VODML"    
    MODEL = namespace + "MODEL"    
    GLOBALS = namespace + "GLOBALS"    
    TEMPLATES = namespace + "TEMPLATES"
    INSTANCE = namespace + "INSTANCE"
    ATTRIBUTE = namespace + "ATTRIBUTE"
    COLLECTION = namespace + "COLLECTION"
    JOIN = namespace + "JOIN"
    REFERENCE = namespace + "REFERENCE"
    WHERE = namespace + "WHERE"
    NOROLE = "NOROLE"
    
    
class Att(object):
    '''
    classdocs
    '''
    dmrole = "dmrole"
    dmtype = "dmtype"
    dmid = "dmid"
    name = "name"
    value = "value"
    dmref = "dmref"
    tableref = "tableref"
    ref = "ref"
    primarykey = "primarykey"
    foreignkey = "foreignkey"
    
def key_match(searched_key, key_set):
    if isinstance(key_set, list):
        for key in key_set:
            if key.startswith(searched_key) is True:
                return key
    else: 
        return key_set.startswith(searched_key)
    return None
        
