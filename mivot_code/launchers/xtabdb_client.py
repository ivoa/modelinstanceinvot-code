'''
Created on 1 Jul 2022

@author: laurentmichel
'''
import sys, os, urllib.parse, urllib.request, tempfile
from astropy.io.votable import parse
from mivot_code.client.xml_interpreter.model_viewer import ModelViewer
from mivot_code.client.class_wrappers.mango.mango_parameter import MangoObject

def main():
    if len(sys.argv) != 2:
        print("USAGE: xcatdb_client 'query'")
        sys.exit(1)
    query = urllib.parse.quote_plus(sys.argv[1])
    url = "https://xcatdb.unistra.fr/xtapdb/sync"    
    params = {
        "REQUEST": "doQuery",
        "FORMAT": "application/mango",
        "PHASE": "RUN",
        "LANG": "ADQL",
        "QUERY": sys.argv[1]
        }
    query_string = urllib.parse.urlencode( params )    
    data = query_string.encode( "ascii" )    
    
    tmpfilename = tempfile.NamedTemporaryFile(suffix='.xml').name
    print(data)
    with open(tmpfilename, "w") as tmpfile:
        with urllib.request.urlopen( url, data ) as response:     
            response_text = response.read().decode("utf-8")      
            tmpfile.write(response_text)
            print(response_text)
            votable = parse(tmpfilename)
        
            mviewer = None
            for resource in votable.resources:
                mviewer = ModelViewer(resource, 
                                      votable_path=tmpfilename)
                break;
            mviewer.connect_table(None)
            _ = mviewer.get_next_row()       

            mango_object = None
            for mango_type in mviewer.get_model_component_by_type("mango:MangoObject"):
                print("============================")
                mango_object = MangoObject(mango_type)
                break
        
            for mango_parameter in mango_object._parameters:
                print(mango_parameter)

if __name__ == '__main__':
    main()