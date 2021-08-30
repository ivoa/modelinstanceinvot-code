'''

Read an annotated VOTABLE and show different outputs
Created on 31 mars 2020

@author: laurentmichel
'''

import os, sys, urllib3, time, re
import tempfile
from client.parser.mango_browser import MangoBrowser

file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from utils.dict_utils import DictUtils
from client.inst_builder.vodml_instance import VodmlInstance


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    
    url = "http://viz-beta.u-strasbg.fr/viz-bin/Mango?-source=IX/45/csc11&-out.max=10"
    tf = tempfile.NamedTemporaryFile(suffix='.vot', prefix=os.path.basename(__file__))
    
    content = ""
    while content == "":
        print(">>>>>> try " )
        http = urllib3.PoolManager()
        resp = http.request('GET', url)
        content = resp.data.decode('utf-8')
        time.sleep(2)
    print(">>>>>> Got it " )
    content = content.replace('mango:Source', 'mango:MangoObject')
    content = content.replace('mango:MangoObject.Parameter.measure', 'mango:Parameter.measure')
    content = content.replace('dmrole="coords.SpaceFrame"' ,  'dmtype="coords.SpaceFrame"')
    content = content.replace('"ango:WebEndPpoint"', '"mango:WebEndPpoint"')
    content = content.replace('meas:Measure', 'mango:Parameter.measure')
    content = content.replace('WebEndPpoint', 'WebEndpoint')
    content = content.replace('ContentType', 'contentType')
    content = content.replace("mango:WebEndpoint.url", "mango:WebEndpoint.uri")
 
    tempfile = open(tf.name, 'w')
    tempfile.write(content)
    tempfile.close()

    print ("=== VOTable saved in {}".format(tf.name))
    
    mango_browser = MangoBrowser(tf.name) 
    
    mango_parameters = mango_browser.get_parameters()
    print("======== Parameters ")
    DictUtils.print_pretty_json(mango_parameters)
    
    associated_data = mango_browser.get_associated_data()
    print("======== Associated data ")
    DictUtils.print_pretty_json(associated_data)
    
    print("======== 1st row data ")
    mango_data = mango_browser.get_data_columns()
    DictUtils.print_pretty_json(mango_data)

    sys.exit()
    
    f = open(tf.name, "r")
    votable_path = tf.name
    vodml_instance = VodmlInstance(votable_path, exit_validation=False)
    vodml_instance.populate_templates(resolve_dmrefs=True)
    vodml_instance.connect_join_iterators()
    #os.remove(votable_path)
    
    instance = vodml_instance.get_root_element("mango:MangoObject")
    if instance is None:
        raise Exception("No root element found")

    
    print("=== Mapping of the columns")
    print(instance.get_flatten_data_head())
    # print(instance.get_data_subset_keys())
    print("=== First row: flatten mode")
    inst = None
    while True:
        inst = instance._get_next_row_instance()
        if inst != None:
            break
        else:
            break

    mangoBrowser = MangoBrowser(inst)
    print(DictUtils.get_pretty_json(mangoBrowser.get_parameter_list(pretty_print=True)))
    print(DictUtils.get_pretty_json(mangoBrowser.get_associated_data_list(pretty_print=True)))
    sys.exit(1)

    print("=== Second row: instance mode")
    while True:
        inst = instance._get_next_row_instance()
        if inst != None:
            print(DictUtils.get_pretty_json(inst))
            break
        else:
            break
    
''