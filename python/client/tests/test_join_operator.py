"""
Created on 8 sept. 2021

@author: michel
"""
import os, unittest
from astropy.io.votable import parse

from client.objectbuilder.join_iterator import JoinIterator


class Test(unittest.TestCase):
    def testJoinOperator(self):
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/rich_instance.xml")
        votable = parse(self.votable_path)

        for resource in votable.resources:
            for table in resource.tables:
                if table.name == "Spectra":
                    parsed_table = table
                    break

        join_iterator = JoinIterator(
            {
                "dm-mapping:JOIN": {
                    "@tableref": "Spectra",
                    "dm-mapping:WHERE": {
                        "@foreignkey": "_foreign_spectra",
                        "@primarykey": "_poserr_148",
                    },
                },
                "test:spectrum": {
                    "@dmtype": "test:Spectrum",
                    "test:spectrum.id": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_foreign_spectra",
                        "@value": "",
                    },
                    "test:spectrum.num": {
                        "@dmtype": "ivoa:string",
                        "@ref": "_spc_148",
                        "@value": "",
                    },
                },
            },
        )

        join_iterator.connect_votable(parsed_table)

        self.assertDictEqual(
            join_iterator.table_mapper.json,
            {
                "dm-mapping:VODML": {
                    "dm-mapping:GLOBALS": {},
                    "dm-mapping:TEMPLATES": {
                        "Spectra": {
                            "@tableref": "Spectra",
                            "dm-mapping:WHERE": {
                                "@primarykey": "_foreign_spectra",
                                "@value": -1,
                            },
                            "root": {
                                "test:spectrum": {
                                    "@dmtype": "test:Spectrum",
                                    "test:spectrum.id": {
                                        "@dmtype": "ivoa:real",
                                        "@ref": "_foreign_spectra",
                                        "@value": "array coucou",
                                    },
                                    "test:spectrum.num": {
                                        "@dmtype": "ivoa:string",
                                        "@ref": "_spc_148",
                                        "@value": "array coucou",
                                    },
                                }
                            },
                        }
                    },
                }
            },
        )
        join_iterator.set_foreignkey_value(1)
        self.assertDictEqual(
            join_iterator.table_mapper._get_next_row_instance(),
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
        )

        self.assertDictEqual(
            join_iterator.table_mapper._get_next_row_instance(),
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
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
