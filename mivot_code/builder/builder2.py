'''
Created on 22 Dec 2022

@author: laurentmichel
'''
import xmltodict
import os
from lxml import etree
from mivot_code.utils.xml_utils import XmlUtils

class Constraints:
    def __init__(self, model_name):
        self.datatype = None
        self.role = None
        self.model_name = model_name
        self.constraints = {}

    def add_constraint(self, ele):
        self.datatype = ele.xpath(".//datatype/vodml-ref")[0].text
        self.role = ele.xpath(".//role/vodml-ref")[0].text.replace(self.model_name + ":", "")
        self.constraints[self.role] = self.datatype
        print(f"add constraint on role {self.role}: type={self.datatype} ")
        
    def get_contraint(self, const_key):
        print(f"look for const {const_key} in {self.constraints.keys()}")
        for key in self.constraints.keys():
            if const_key.endswith(key):
                print(f"  found as {self.constraints[key]}")
                return  self.constraints[key]
        print("  not found")
        return None
    
    def get_superclass_contraint(self, const_key):
        print(f"look for const {const_key} in {self.constraints.keys()}")
        stripped_key = const_key.replace(self.model_name + ":", "")
        for key in self.constraints.keys():
            if key.startswith(stripped_key) is True:
                print(f"  found SC as {self.constraints[key]}")
                return  self.constraints[key]
        print("  not found")
        return None
    
class Builder:
    def __init__(self, model_name, class_name, vodml_path, output_dir):
        self.model_name = model_name
        self.vodml = XmlUtils.xmltree_from_file(vodml_path)
        self.output_dir = output_dir
        self.output = None
        self.outputname = None
        self.constraints = Constraints(model_name)
        self.class_name = class_name
        
    def build(self):
        
         
        for ele in self.vodml.xpath(f'.//dataType'):
            for tags in ele.getchildren  (): 
                if tags.tag == "vodml-id" and  tags.text == self.class_name :
                    self.build_object(ele, "", True, True)
                    return
                
        for ele in self.vodml.xpath(f'.//objectType'):
            for tags in ele.getchildren  (): 
                if tags.tag == "vodml-id" and  tags.text == self.class_name :
                    self.build_object(ele, "", True, True)
                    return

            
    def build_object(self, ele, role, root, aggregate):
        for tags in list(ele): 
            if tags.tag == "constraint":
                self.constraints.add_constraint(tags)
                break
        for tags in list(ele): 
            print(f"   TAG {tags.tag}")
            if tags.tag == "vodml-id":
                print(f"== build {tags.text}")                    
                if root is True:
                    self.outputname = os.path.join(
                    self.output_dir, 
                    self.model_name + "." + tags.text + ".xml"
                    )
                    print(f"opening {self.model_name}.{tags.text}.xml")
                    self.output = open(self.outputname, "w")
                if aggregate is True:
                    if role == "coords:Coordinate.coordSys":
                        self.write_out("<!-- The Coordinate system can be pushed up to the GLOBALS and replaced here with a REFERENCE-->")
                    self.write_out(f'<INSTANCE dmrole="{role}" dmtype="{self.model_name}:{tags.text}">')
            elif tags.tag == "extends":
                self.addExtend(tags)
            elif tags.tag == "reference":
                self.addReference(tags)
            elif tags.tag == "composition":
                self.addComposition(tags)
            elif tags.tag == "attribute":
                self.addAttribute(tags)
            elif tags.tag == "description":
                if aggregate is True:
                    self.write_out(f'<!-- {tags.text}" -->')
                
        if aggregate is True:
            self.write_out("</INSTANCE>")
        if root is True:
            self.output.close()
            XmlUtils.xmltree_to_file(XmlUtils.xmltree_from_file(self.outputname), self.outputname)
          
    def addReference(self, ele):
        print("== Add reference")
        vodmlid = None
        for tags in ele.getchildren():        
            if tags.tag == "vodml-id":
                vodmlid = tags.text
            elif tags.tag == "datatype":
                for dttag in list(tags):
                    if dttag.tag == "vodml-ref":
                        reftype = dttag.text.replace(self.model_name + ":", "")
                        break
        vokey = self.model_name + ":" + vodmlid
        const_type = self.constraints.get_contraint(vokey) 

        if const_type is not None:
            reftype = const_type
        self.get_object_by_ref(reftype.replace(self.model_name + ":", ""),
                               self.model_name + ":" + vodmlid, True)
            
    def addComposition(self, ele):
        print("== Add composition")
        vodmlid = None
        for tags in ele.getchildren():        
            if tags.tag == "vodml-id":
                vodmlid = tags.text
            elif tags.tag == "multiplicity":
                max = tags.xpath(".//maxOccurs")[0].text
            elif tags.tag == "datatype":
                for dttag in list(tags):
                    if dttag.tag == "vodml-ref":
                        reftype = dttag.text.replace(self.model_name + ":", "")
                        break
        vokey = self.model_name + ":" + vodmlid
        const_type = self.constraints.get_contraint(vokey) 

        if const_type is not None:
            reftype = const_type
        if max != "1":
            self.write_out(f'<COLLECTION dmrole="{(self.model_name + ":" + vodmlid)}" >')
            self.get_object_by_ref(reftype.replace(self.model_name + ":", ""),
                               "", True)
            self.write_out("</COLLECTION>")
            return
        self.get_object_by_ref(reftype.replace(self.model_name + ":", ""),
                               self.model_name + ":" + vodmlid, True)
            
    def addExtend(self, ele):
        """if constraint is not None:
            self.get_object_by_ref(constraint.datatype.replace(self.model_name + ":", ""))
            return
        """
        print("== add extend")
        for tags in ele.getchildren  (): 
            if tags.tag == "vodml-ref":
                reftype = tags.text
                break
            
        const_type = self.constraints.get_contraint(reftype) 
        if const_type is not None in self.constraints.constraints:
            reftype = const_type
        self.get_object_by_ref(reftype.replace(self.model_name + ":", ""), reftype, False)
                
    def addAttribute(self, ele):
        for tags in ele.getchildren  ():         # root is the ElementTree object
            if tags.tag == "vodml-id":
                vodml_id = tags.text
            elif tags.tag == "datatype" :   
                for ref in tags.getchildren():
                    vodmlref = ref.text  
                    break
        self.write_out(f'<ATTRIBUTE dmrole="{self.model_name}:{vodml_id}" dmtype="{self.model_name}:{vodmlref}" unit="" ref="@@@@@" value=""/>')
    
    def get_object_by_ref(self, vodmlid, role, aggregate):
        print(f"search object with vodmlid={vodmlid}")
        for ele in self.vodml.xpath(f'.//objectType'):
            for tags in list(ele):  
                if tags.tag == "vodml-id" and tags.text == vodmlid:
                    print("  found in objecttype")
                    self.build_object(ele, role, False, aggregate)
                    return
        for ele in self.vodml.xpath(f'.//dataType'):
            for tags in list(ele):         # root is the ElementTree object
                if tags.tag == "vodml-id" and tags.text == vodmlid:
                    print("  found in datatype")
                    self.build_object(ele, role, False, aggregate)
                    return
        print("not found")

    def write_out(self, string):
        if self.output is None:
            print(string)
        else:
            self.output.write(string) 
            self.output.write("\n") 

    def is_abstract(self, ele):
        print(f' abbbb {ele.get("abstract")}')
        return ele.get("abstract") is not None
    
if __name__ == '__main__':
    builder = Builder(
        "coords",
        "JD",
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "Coords-v1.0.vo-dml.xml"
            ),
            os.path.dirname(os.path.realpath(__file__))
        )
    builder.build()


    
    