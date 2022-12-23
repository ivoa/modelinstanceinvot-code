'''
Created on 22 Dec 2022

@author: laurentmichel
'''
import xmltodict
import os
from lxml import etree
from mivot_code.utils.xml_utils import XmlUtils

class Constraint:
    def __init__(self, ele):
        XmlUtils.pretty_print(ele)
        self.datatype = ele.xpath(".//datatype/vodml-ref")[0].text
        self.role = ele.xpath(".//role/vodml-ref")[0].text
        print(f"role {self.role} type {self.datatype} ")

        
class Builder:
    def __init__(self, model_name, vodml_path, output_dir):
        self.model_name = model_name
        self.vodml = XmlUtils.xmltree_from_file(vodml_path)
        self.output_dir = output_dir
        self.output = None
        self.outputname = None
        
    def build(self):
        
        for ele in self.vodml.xpath(f'.//objectType'):
            break
            if self.is_abstract(ele) is False:
                self.build_object(ele, True, False)
        
        for ele in self.vodml.xpath(f'.//dataType'):
            for tags in ele.getchildren  (): 
                if tags.tag == "vodml-id" and  tags.text == "Coordinate" :
                    if self.is_abstract(ele) is False or True is True:
                        self.build_object(ele, True, False)

            
    def build_object(self, ele, root, insert):
        XmlUtils.pretty_print(ele)
        constraint = None
        for tags in list(ele): 
            if tags.tag == "constraint":
                constraint = Constraint(tags)
                break
        for tags in ele.getchildren  (): 
            print(tags.tag)
            if tags.tag == "vodml-id":
                if root is True:
                    self.outputname = os.path.join(
                    self.output_dir, 
                    self.model_name + "." + tags.text + ".xml"
                    )
                    print(f"opening {self.model_name}.{tags.text}.xml")
                    self.output = open(self.outputname, "w")
                if insert is False:
                    self.write_out(f'<INSTANCE dmrole="" dmtype="{self.model_name}:{tags.text}">')
            elif tags.tag == "description":
                self.write_out(f'<!-- {tags.text}" -->')
            elif tags.tag == "extends":
                self.addExtend(tags, constraint)
            elif tags.tag == "attribute":
                self.addAttribute(tags)
            elif tags.tag == "reference":
                print(">>>>>>>>>>>>>")
                self.addReference(tags)
            else:
                print(f"unprocessed {tags.tag}")

        if insert is False:
            self.write_out("</INSTANCE>")
        if root is True:
            self.output.close()
            XmlUtils.xmltree_to_file(XmlUtils.xmltree_from_file(self.outputname), self.outputname)
        
    def addReference(self, ele):
        for tags in ele.getchildren():        
            if tags.tag == "vodml-id":
                vodmlid = tags.text
                print(tags.text)
            elif tags.tag == "datatype":
                print(tags.text)
                XmlUtils.pretty_print(tags)
                for dttag in list(tags):
                    if dttag.tag == "vodml-ref":
                        reftype = dttag.text
                        break
        self.get_object_by_ref(reftype.replace(self.model_name + ":", ""))
            
    def addExtend(self, ele, constraint):
        """if constraint is not None:
            self.get_object_by_ref(constraint.datatype.replace(self.model_name + ":", ""))
            return
        """
        for tags in ele.getchildren  (): 
            print("   "+ tags.tag)        
            if tags.tag == "vodml-ref":
                print(f"add extend {tags.text}")
                vodmlid = self.get_object_by_ref(tags.text.replace(self.model_name + ":", ""))
                
    def addAttribute(self, ele):
        for tags in ele.getchildren  ():         # root is the ElementTree object
            if tags.tag == "vodml-id":
                vodml_id = tags.text
            elif tags.tag == "datatype" :   
                for ref in tags.getchildren():
                    vodmlref = ref.text  
                    break
        self.write_out(f'<ATTRIBUTE dmrole="{self.model_name}:{vodml_id}" dmtype="{self.model_name}:{vodmlref}" unit="" ref="@@@@@" value=""/>')
    
    def get_object_by_ref(self, ref):
        print(f"search object by ref {ref}")
        for ele in self.vodml.xpath(f'.//objectType'):
            """
            if self.is_abstract(ele) is True:
                self.write_out(f'<ABSTRACT_REFERENCE ref="{ref}" />')
                print(f'<ABSTRACT_REFERENCE ref="{ref}" />')
                return
            """
            for tags in ele.getchildren  ():  
                if tags.tag == "vodml-id" and tags.text == ref:
                    self.build_object(ele, False, True)
                    return
        for ele in self.vodml.xpath(f'.//dataType'):
            for tags in ele.getchildren  ():         # root is the ElementTree object
                print(f"{ref} -> {tags.text} {tags.tag}" )      # root is the ElementTree object
                if tags.tag == "vodml-id" and tags.text == ref:
                    self.build_object(ele, False, True)
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
    builder = Builder("coords", 
                      os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "Coords-v1.0.vo-dml.xml"
            ),
            os.path.dirname(os.path.realpath(__file__))
        )
    builder.build()


    
    