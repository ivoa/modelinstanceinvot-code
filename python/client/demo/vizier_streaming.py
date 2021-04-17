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
    # associated parameters
    content = content.replace('meas:Measure', 'mango:Parameter.measure')
    #content = content.replace('"J2000" dmrole="">', '"J2000" dmtype="coords.SpaceFrame">')
    #content = re.sub(r"(?s)<INFO>.*?</INFO>", r"", content, re.MULTILINE)

    #content = content.replace("<INFO>", "")
    #ßcontent = content.replace("</INFO>", "")
    #content = content.replace("The MODEL_INSTANCE section of this document is a VizieR prototype using MangoDM -", "")
    #content = content.replace("The relevance of metadata exposed as well as the current serialization is not guaranteed.", "")
    #
    tempfile = open(tf.name, 'w')
    tempfile.write(content)
    tempfile.close()

    print ("=== VOTable saved in {}".format(tf.name))
    
    
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