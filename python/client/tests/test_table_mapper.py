"""
Created on 1 sept. 2021

@author: michel
"""
import os, json
import unittest
from client.objectbuilder.vodml_instance import VodmlInstance
from client.objectbuilder.table_mapper import TableMapper
from astropy.io.votable import parse
from utils.dict_utils import DictUtils


class Test(unittest.TestCase):
    def testName(self):
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/rich_instance.xml")
        votable = parse(self.votable_path)
        vodml_instance = VodmlInstance(self.votable_path)

        for resource in votable.resources:
            for table in resource.tables:
                break

        table_mapper = TableMapper(
            table.name, self.votable_path, json_inst_dict=vodml_instance.json_view
        )
        # table_mapper.resolve_refs_and_values()
        table_mapper._set_header_values(table_mapper.table_json)

        table_mapper._set_table_iterators(table_mapper.table_json)
        table_mapper._set_array_subelement_values(table_mapper.array, parent_role=None)
        table_mapper.map_columns()
        print(table_mapper.column_mapping)

        self.assertDictContainsSubset(
            {
                "index": 0,
                "parent_role": None,
                "parent_type": None,
                "role": "test:detection.num",
                "ucd": "meta.id;meta.main",
            },
            table_mapper.column_mapping.column_refs["_poserr_148"],
        )
        self.assertDictEqual(
            json.loads(json.dumps(table_mapper.column_mapping.column_ids)),
            {
                "0": {
                    "id": "_poserr_148",
                    "name": "oidsaada",
                    "ref": None,
                    "ucd": "meta.id;meta.main",
                }
            },
        )
        table_mapper._set_join_iterators(table_mapper.table_json)
        self.assertEqual(
            list(table_mapper.join_iterators.keys()), ["OtherResults", "Spectra"]
        )
        self.assertEqual(
            table_mapper.join_iterators["OtherResults"].__repr__(),
            "Join iterator f_table=OtherResults p_key=_poserr_148, f_key=_foreign_other",
        )
        self.assertEqual(
            table_mapper.join_iterators["Spectra"].__repr__(),
            "Join iterator f_table=Spectra p_key=_poserr_148, f_key=_foreign_spectra",
        )
        for key, value in table_mapper.join_iterators.items():
            for resource in votable.resources:
                for table in resource.tables:
                    if table.name == key:
                        value.connect_votable(table)
                        break

        self.assertDictEqual(
            table_mapper._get_next_row_instance(),
            {
                "@ID": "_point",
                "@dmtype": "Point",
                "test.detections": [
                    {
                        "test:detection": {
                            "@dmtype": "test:Detection",
                            "test:detection.id": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_foreign_other",
                                "@value": 1,
                            },
                            "test:detection.num": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_num_148",
                                "@value": 11,
                            },
                        }
                    },
                    {
                        "test:detection": {
                            "@dmtype": "test:Detection",
                            "test:detection.id": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_foreign_other",
                                "@value": 1,
                            },
                            "test:detection.num": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_num_148",
                                "@value": 12,
                            },
                        }
                    },
                ],
                "test.spectra": [
                    {
                        "test:spectrum": {
                            "@dmtype": "test:Spectrum",
                            "test:spectrum.id": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_foreign_spectra",
                                "@value": 1,
                            },
                            "test:spectrum.num": {
                                "@dmtype": "ivoa:string",
                                "@ref": "_spc_148",
                                "@value": "Spectrum 11",
                            },
                        }
                    },
                    {
                        "test:spectrum": {
                            "@dmtype": "test:Spectrum",
                            "test:spectrum.id": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_foreign_spectra",
                                "@value": 1,
                            },
                            "test:spectrum.num": {
                                "@dmtype": "ivoa:string",
                                "@ref": "_spc_148",
                                "@value": "Spectrum 12",
                            },
                        }
                    },
                ],
                "test:detection.num": {
                    "@dmtype": "ivoa:real",
                    "@ref": "_poserr_148",
                    "@value": 1,
                },
            },
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
