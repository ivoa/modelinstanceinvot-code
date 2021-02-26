'''
Created on Sep 17, 2020

@author: laurentmichel
'''
import unittest
import os

from product_annoter.mapper.constants import PARAM_TABLE_MAPPING
from product_annoter.mapper.parameter_appender import ParameterAppender

output_mapping_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
        "data",
        "test_param_appender.xml")


def get_refs(mango_tree, host_role, value_role):
    retour = []
    blocks = mango_tree.xpath("//INSTANCE[@dmrole='" + host_role + "']")
    for block in blocks:
        subblocks = block.xpath(".//ATTRIBUTE[@dmrole='" + value_role + "']")
        for subblock in subblocks:
            retour.append(subblock.attrib["ref"])
    return retour


def get_vals(mango_tree, host_role, value_role):
    retour = []
    blocks = mango_tree.xpath("//INSTANCE[@dmrole='" + host_role + "']")
    for block in blocks:
        subblocks = block.xpath(".//ATTRIBUTE[@dmrole='" + value_role + "']")
        for subblock in subblocks:
            retour.append(subblock.attrib["value"])
    return retour


class Test(unittest.TestCase):
    
    def testSetRef(self):
        host_role = "mango:stcextend.LonLatSkyPosition.coord"
        value_role = "mango:stcextend.LonLatPoint.longitude"

        appender = ParameterAppender(
            PARAM_TABLE_MAPPING.POSITION,
            output_mapping_path,
            None
            )
        appender.set_ref(host_role, value_role, "ra_ref")
        self.assertListEqual(get_refs(appender.mango_tree, host_role, value_role), ['ra_ref'])
        # print(etree.tostring(appender.mango_tree, encoding="unicode", pretty_print=True))
        
    def testSetValue(self):
        host_role = "mango:stcextend.LonLatSkyPosition.coord"
        value_role = "mango:stcextend.LonLatPoint.longitude"

        appender = ParameterAppender(
            PARAM_TABLE_MAPPING.POSITION,
            output_mapping_path,
            None
            )
        appender.set_value(host_role, value_role, "ra_val")
        self.assertListEqual(get_vals(appender.mango_tree, host_role, value_role), ['ra_val'])
        # print(etree.tostring(appender.mango_tree, encoding="unicode", pretty_print=True))
        
    @classmethod
    def setUpClass(cls):
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
