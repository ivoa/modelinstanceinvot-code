"""
Created on 1 sept. 2021

@author: michel
"""
import os
import unittest
from utils.dict_utils import DictUtils
from client.objectbuilder.vodml_instance import VodmlInstance


class Test(unittest.TestCase):
    def testName(self):
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/rich_instance.xml")
        vodml_instance = VodmlInstance(self.json_path)

        self.assertListEqual(
            list(vodml_instance.table_mappers.keys()),
            ["Results", "OtherResults", "Spectra"],
        )

        # DictUtils.print_pretty_json(vodml_instance.table_mappers["Results"].json)
        vodml_instance.get_root_element("test.model")
        self.assertDictEqual(
            vodml_instance.json_view,
            {
                "@dmtype": "test.model",
                "test.header": {
                    "@dmtype": "test.Header",
                    "test.frame": {
                        "@ID": "SpaceFrame_ICRS",
                        "@dmtype": "coords:SpaceFrame",
                        "coords:SpaceFrame.equinox": {
                            "@dmtype": "coords:Epoch",
                            "@value": "NoSet",
                        },
                        "coords:SpaceFrame.refPosition": {
                            "@dmtype": "coords:StdRefLocation",
                            "coords:StdRefLocation.position": {
                                "@dmtype": "ivoa:string",
                                "@value": "NoSet",
                            },
                        },
                        "coords:SpaceFrame.spaceRefFrame": {
                            "@dmtype": "ivoa:string",
                            "@value": "ICRS",
                        },
                    },
                    "test.owner": {
                        "@dmtype": "test.Owner",
                        "test.owner.firstname": {
                            "@dmtype": "string",
                            "@value": "Laurent",
                        },
                        "test.owner.name": {"@dmtype": "string", "@value": "Michel"},
                        "test.title": {
                            "@dmtype": "string",
                            "@ref": "_title",
                            "@value": "",
                        },
                    },
                    "test.points": [{"dm-mapping:JOIN": {"@tableref": "Results"}}],
                },
            },
        )

        self.assertDictEqual(
            vodml_instance.get_instance(),
            {
                "@dmtype": "test.model",
                "test.header": {
                    "@dmtype": "test.Header",
                    "test.frame": {
                        "@ID": "SpaceFrame_ICRS",
                        "@dmtype": "coords:SpaceFrame",
                        "coords:SpaceFrame.equinox": {
                            "@dmtype": "coords:Epoch",
                            "@value": "NoSet",
                        },
                        "coords:SpaceFrame.refPosition": {
                            "@dmtype": "coords:StdRefLocation",
                            "coords:StdRefLocation.position": {
                                "@dmtype": "ivoa:string",
                                "@value": "NoSet",
                            },
                        },
                        "coords:SpaceFrame.spaceRefFrame": {
                            "@dmtype": "ivoa:string",
                            "@value": "ICRS",
                        },
                    },
                    "test.owner": {
                        "@dmtype": "test.Owner",
                        "test.owner.firstname": {
                            "@dmtype": "string",
                            "@value": "Laurent",
                        },
                        "test.owner.name": {"@dmtype": "string", "@value": "Michel"},
                        "test.title": {
                            "@dmtype": "string",
                            "@ref": "_title",
                            "@value": "",
                        },
                    },
                    "test.points": [
                        {"dm-mapping:JOIN": {"@tableref": "Results"}},
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
                    ],
                },
            },
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
