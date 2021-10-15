"""
Created on 1 sept. 2021

@author: michel
"""
import os
import unittest
from collections import OrderedDict

from client.objectbuilder.table_iterator import TableIterator
from astropy.io.votable import parse
from client.objectbuilder.column_mapping import ColumnMapping

class Test(unittest.TestCase):
    def testName(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/rich_instance.xml")
        votable = parse(self.votable_path)
        for resource in votable.resources:
            for table in resource.tables:
                parsed_table = table
                break

        column_mapping = ColumnMapping()
        column_mapping.column_ids = OrderedDict(
            [
                (
                    0,
                    {
                        "name": "oidsaada",
                        "ref": None,
                        "id": "_poserr_148",
                        "ucd": "meta.id;meta.main",
                    },
                )
            ]
        )
        column_mapping.column_refs = OrderedDict(
            [
                (
                    "_poserr_148",
                    {
                        "parent_role": None,
                        "parent_type": None,
                        "role": "test:detection.num",
                        "index": 0,
                        "field": '<FIELD ID="_poserr_148" datatype="long" name="oidsaada" ucd="meta.id;meta.main"/>',
                        "ucd": "meta.id;meta.main",
                    },
                )
            ]
        )
        table_iterator = TableIterator(
            "iterator_key",
            parsed_table.to_table(),
            {
                "@tableref": "Results",
                "primary:point": {
                    "@ID": "_point",
                    "@dmtype": "Point",
                    "test.detections": [
                        {
                            "dm-mapping:JOIN": {
                                "@tableref": "OtherResults",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                            "test:detection": {
                                "@dmtype": "test:Detection",
                                "test:detection.id": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                    "@value": "",
                                },
                                "test:detection.num": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_num_148",
                                    "@value": "",
                                },
                            },
                        }
                    ],
                    "test.spectra": [
                        {
                            "dm-mapping:JOIN": {
                                "@tableref": "Spectra",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                            "test:spectrum": {
                                "@dmtype": "test:Spectrum",
                                "test:spectrum.id": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                    "@value": "",
                                },
                                "test:spectrum.num": {
                                    "@dmtype": "ivoa:string",
                                    "@ref": "_spc_148",
                                    "@value": "",
                                },
                            },
                        }
                    ],
                    "test:detection.num": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_poserr_148",
                        "@value": "",
                    },
                },
            },
            column_mapping,
            row_filter=None,
        )
        self.assertEqual(table_iterator._get_next_row()[0], 1)
        self.assertEqual(table_iterator._get_next_row()[0], 2)

        table_iterator._rewind()
        self.assertListEqual(table_iterator._get_next_flatten_row(), [1])
        self.assertListEqual(table_iterator._get_next_flatten_row(), [2])

        table_iterator._rewind()
        self.assertDictEqual(
            table_iterator._get_next_row_instance(),
            {
                "@tableref": "Results",
                "primary:point": {
                    "@ID": "_point",
                    "@dmtype": "Point",
                    "test.detections": [
                        {
                            "dm-mapping:JOIN": {
                                "@tableref": "OtherResults",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                            "test:detection": {
                                "@dmtype": "test:Detection",
                                "test:detection.id": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                    "@value": "",
                                },
                                "test:detection.num": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_num_148",
                                    "@value": "",
                                },
                            },
                        }
                    ],
                    "test.spectra": [
                        {
                            "dm-mapping:JOIN": {
                                "@tableref": "Spectra",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                            "test:spectrum": {
                                "@dmtype": "test:Spectrum",
                                "test:spectrum.id": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                    "@value": "",
                                },
                                "test:spectrum.num": {
                                    "@dmtype": "ivoa:string",
                                    "@ref": "_spc_148",
                                    "@value": "",
                                },
                            },
                        }
                    ],
                    "test:detection.num": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_poserr_148",
                        "@value": 1,
                    },
                },
            },
        )

        self.assertDictEqual(
            table_iterator._get_next_row_instance(),
            {
                "@tableref": "Results",
                "primary:point": {
                    "@ID": "_point",
                    "@dmtype": "Point",
                    "test.detections": [
                        {
                            "dm-mapping:JOIN": {
                                "@tableref": "OtherResults",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                            "test:detection": {
                                "@dmtype": "test:Detection",
                                "test:detection.id": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                    "@value": "",
                                },
                                "test:detection.num": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_num_148",
                                    "@value": "",
                                },
                            },
                        }
                    ],
                    "test.spectra": [
                        {
                            "dm-mapping:JOIN": {
                                "@tableref": "Spectra",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                            "test:spectrum": {
                                "@dmtype": "test:Spectrum",
                                "test:spectrum.id": {
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                    "@value": "",
                                },
                                "test:spectrum.num": {
                                    "@dmtype": "ivoa:string",
                                    "@ref": "_spc_148",
                                    "@value": "",
                                },
                            },
                        }
                    ],
                    "test:detection.num": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_poserr_148",
                        "@value": 2,
                    },
                },
            },
        )

        self.assertListEqual(
            table_iterator._get_flatten_data_head(),
            ["None (None->test:detection.num) [col#0 _poserr_148 (meta.id;meta.main)]"],
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
