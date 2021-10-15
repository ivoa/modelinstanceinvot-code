"""
Created on 13 sept. 2021

@author: michel
"""
import unittest
from utils.dict_utils import DictUtils

from client.objectbuilder.reference_resolver import ReferenceResolver

class Test(unittest.TestCase):
    def testReferenceResolver(self):
        json_block = {
            "dm-mapping:GLOBALS": {
                "SpaceFrame_ICRS": {
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
                "root": {
                    "@dmtype": "test.model",
                    "test.header": {
                        "@dmtype": "test.Header",
                        "dm-mapping:REFERENCE": {
                            "@dmref": "SpaceFrame_ICRS",
                            "@dmrole": "test.frame",
                        },
                        "test.owner": {
                            "@dmtype": "test.Owner",
                            "test.owner.firstname": {
                                "@dmtype": "string",
                                "@value": "Laurent",
                            },
                            "test.owner.name": {
                                "@dmtype": "string",
                                "@value": "Michel",
                            },
                            "test.title": {
                                "@dmtype": "string",
                                "@ref": "_title",
                                "@value": "",
                            },
                        },
                        "test.points": [{"dm-mapping:JOIN": {"@tableref": "Results"}}],
                    },
                },
            }
        }

        ReferenceResolver.resolve_object_references(json_block)
        self.assertDictEqual(
            json_block,
            {
                "dm-mapping:GLOBALS": {
                    "SpaceFrame_ICRS": {
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
                    "root": {
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
                                "test.owner.name": {
                                    "@dmtype": "string",
                                    "@value": "Michel",
                                },
                                "test.title": {
                                    "@dmtype": "string",
                                    "@ref": "_title",
                                    "@value": "",
                                },
                            },
                            "test.points": [
                                {"dm-mapping:JOIN": {"@tableref": "Results"}}
                            ],
                        },
                    },
                }
            },
        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReferenceResolver']
    unittest.main()
