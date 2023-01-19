'''
Created on 22 Dec 2022

@author: laurentmichel
'''
import xmltodict
import os
from lxml import etree
from mivot_code.utils.xml_utils import XmlUtils

DEFAULT_CONCRETE_CLASSES = {
    "RefLocation": "StdRefLocation"
    }

class Constraints:
    def __init__(self, model_name):
        self.datatype = None
        self.role = None
        self.model_name = model_name
        self.constraints = {}

    def add_constraint(self, ele):
        refs = ele.xpath(".//datatype/vodml-ref")
        if len(refs) == 0:
            return
        self.datatype = refs[0].text
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
        print(f"build object with role={role}")
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
                    dmid=""
                    if role == "coords:Coordinate.coordSys":
                        self.write_out(f'<!-- The Coordinate system can be pushed up to the GLOBALS and replaced here with <REFERENCE dmref="SOME_REF" dmrole="{role}" />">-->')
                        dmid = 'dmid="PUT_AN_ID_HERE"'
                    self.write_out(f'<INSTANCE {dmid} dmrole="{role}" dmtype="{self.model_name}:{tags.text}">')
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
                
        if aggregate is True :
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
    
        print("== add extend")
        for tags in ele.getchildren  (): 
            if tags.tag == "vodml-ref":
                reftype = tags.text
                break
            
        const_type = self.constraints.get_contraint(reftype) 
        if const_type is not None in self.constraints.constraints:
            reftype = const_type
        self.get_object_by_ref(reftype.replace(self.model_name + ":", ""), reftype, False, extend=True)
                
    def addAttribute(self, ele):
        for tags in ele.getchildren  ():         # root is the ElementTree object
            if tags.tag == "vodml-id":
                vodml_id = tags.text
                dmrole = f"{self.model_name}:{vodml_id}"
            elif tags.tag == "datatype" :   
                for ref in tags.getchildren():
                    vodmlref = ref.text 
                    if ":" in  vodmlref:
                        dmtype = f"{vodmlref}"
                    else:
                        dmtype = f"{self.model_name}:{vodmlref}"
                    if vodmlref.startswith("ivoa:") is False:
                        self.get_object_by_ref(vodmlref.replace(self.model_name + ":", ""), dmrole, True)
                        return
                    break
        if dmtype.lower().endswith("string"):
            unit_att = ""
        else:
            unit_att = 'unit=""'

        self.write_out(f'<ATTRIBUTE dmrole="{dmrole}" dmtype="{dmtype}" {unit_att} ref="@@@@@" value=""/>')
    
    def get_object_by_ref(self, vodmlid, role, aggregate, extend=False):
        print(f"search object with vodmlid={vodmlid}")
        for ele in self.vodml.xpath(f'.//objectType'):
            abstract_att = ele.get("abstract")
            for tags in list(ele):  
                if tags.tag == "vodml-id" and tags.text == vodmlid:
                    print("  found in objecttype")
                    if extend is False and abstract_att is not None and abstract_att.lower() == "true":
                        self.get_concrete_type_by_ref(vodmlid, role, aggregate, extend)                    
                    else:
                        self.build_object(ele, role, False, aggregate)
                    return

        for ele in self.vodml.xpath(f'.//dataType'):
            abstract_att = ele.get("abstract")
                
            for tags in list(ele):         # root is the ElementTree object
                if tags.tag == "vodml-id" and tags.text == vodmlid:
                    print("  found in datatype")  
                    print(extend)                  
                    if extend is False and abstract_att is not None and abstract_att.lower() == "true":
                        self.get_concrete_type_by_ref(vodmlid, role, aggregate, extend)                    
                    else:
                        self.build_object(ele, role, False, aggregate)
                    return
                        
        for ele in self.vodml.xpath(f'.//primitiveType'):
            found = False
            description = ""
            for tags in list(ele):         # root is the ElementTree object
                if tags.tag == "vodml-id" and tags.text == vodmlid:
                    found = True
                if tags.tag == "description":
                    description = f"<!-- {tags.text} -->"
            if found is True:
                if description:
                    self.write_out(description)
                self.write_out(f'<ATTRIBUTE dmrole="{role}" dmtype="{vodmlid}" ref="@@@@@" value=""/>')
                return
            
        for ele in self.vodml.xpath(f'.//enumeration'):
            found = False
            description = ""
            for tags in list(ele):         # root is the ElementTree object
                if tags.tag == "vodml-id" and tags.text == vodmlid:
                    found = True
                if tags.tag == "description":
                    description = f"<!-- {tags.text} -->"
            if found is True:
                values = ele.xpath(f'.//literal/name')
                val_str = ""
                for value in values:
                    val_str += value.text + " "
                if description:
                    self.write_out(description)
                self.write_out(f'<!-- Enumeration datatype: supported values are {val_str} -->')
                self.write_out(f'<ATTRIBUTE dmrole="{role}" dmtype="{vodmlid}" value="OneOf {val_str}"/>')
                return

        raise Exception(f"Type {vodmlid} not found")

    def get_concrete_type_by_ref(self, abstract_vodmlid, role, aggregate, extend):
        if role.endswith("coordSpace"):
            self.write_out("<!-- the axis representation (coords:PhysicalCoordSys.coordSpace) is not serialized here -->")
        elif abstract_vodmlid in DEFAULT_CONCRETE_CLASSES:
            concrete_type = DEFAULT_CONCRETE_CLASSES[abstract_vodmlid]
            print(f"    Take {concrete_type} as concrete type for {abstract_vodmlid}")
            self.write_out(f"<!-- {concrete_type} taken as concrete type for {abstract_vodmlid} -->")

            self.get_object_by_ref(concrete_type, role, aggregate, extend)
            return
        else:
            raise Exception(f"Cannot found a concrete type for {abstract_vodmlid}")
        
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
        "SpaceSys",
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "Coords-v1.0.vo-dml.xml"
            ),
            os.path.dirname(os.path.realpath(__file__))
        )
    builder.build()


    
    