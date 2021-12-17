"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os
from client.tests import logger
from client.translator.json_mapping_builder import JsonMappingBuilder
from client.translator.vocabulary import Att, Ele
from utils.dict_utils import DictUtils


class Test(unittest.TestCase):
    """
    def test_revert_collection(self):
        json_dict = DictUtils.read_dict_from_file(self.json_path)
        builder = JsonMappingBuilder(json_dict=json_dict)

        builder._revert_collection(
            {
                "dm-mapping:VODML": {
                    "@xmlns:dm-mapping": "http://www.ivoa.net/xml/merged-syntax",
                    "dm-mapping:GLOBALS": {
                        "dm-mapping:INSTANCE": {
                            "@dmrole": "test.header",
                            "@dmtype": "test.Header",
                            "dm-mapping:COLLECTION": {
                                "@dmrole": "test.points",
                                "dm-mapping:JOIN": {"@tableref": "Results"},
                            },
                        }
                    },
                }
            },
            Ele.COLLECTION,
        )
        self.assertDictEqual(
            builder.change_buffer["newcontent"][0],
            {"test.points": [{"dm-mapping:JOIN": {"@tableref": "Results"}}]},
        )

        builder = JsonMappingBuilder(json_dict=json_dict)
        builder._revert_collection(
            {
                "@tableref": "Results",
                "dm-mapping:INSTANCE": {
                    "@ID": "_point",
                    "@dmrole": "primary:point",
                    "@dmtype": "Point",
                    "dm-mapping:ATTRIBUTE": {
                        "@dmrole": "test:detection.num",
                        "@dmtype": "ivoa:real",
                        "@ref": "_poserr_148",
                    },
                    "dm-mapping:COLLECTION": [
                        {
                            "@dmrole": "test.detections",
                            "dm-mapping:INSTANCE": {
                                "@dmrole": "test:detection",
                                "@dmtype": "test:Detection",
                                "dm-mapping:ATTRIBUTE": [
                                    {
                                        "@dmrole": "test:detection.num",
                                        "@dmtype": "ivoa:real",
                                        "@ref": "_num_148",
                                    },
                                    {
                                        "@dmrole": "test:detection.id",
                                        "@dmtype": "ivoa:real",
                                        "@ref": "_foreign",
                                    },
                                ],
                            },
                            "dm-mapping:JOIN": {
                                "@tableref": "OtherResults",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                        },
                        {
                            "@dmrole": "test.spectra",
                            "dm-mapping:INSTANCE": {
                                "@dmrole": "test:spectrum",
                                "@dmtype": "test:Spectrum",
                                "dm-mapping:ATTRIBUTE": [
                                    {
                                        "@dmrole": "test:spectrum.num",
                                        "@dmtype": "ivoa:string",
                                        "@ref": "_spc_148",
                                    },
                                    {
                                        "@dmrole": "test:spectrum.id",
                                        "@dmtype": "ivoa:real",
                                        "@ref": "_foreign",
                                    },
                                ],
                            },
                            "dm-mapping:JOIN": {
                                "@tableref": "Spectra",
                                "dm-mapping:WHERE": {
                                    "@foreignkey": "_foreign",
                                    "@primarykey": "_poserr_148",
                                },
                            },
                        },
                    ],
                },
            },
            Ele.COLLECTION,
        )
        self.assertDictEqual(
            builder.change_buffer["newcontent"][0],
            {
                "test.detections": [
                    {
                        "dm-mapping:INSTANCE": {
                            "@dmrole": "test:detection",
                            "@dmtype": "test:Detection",
                            "dm-mapping:ATTRIBUTE": [
                                {
                                    "@dmrole": "test:detection.num",
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_num_148",
                                },
                                {
                                    "@dmrole": "test:detection.id",
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                },
                            ],
                        },
                        "dm-mapping:JOIN": {
                            "@tableref": "OtherResults",
                            "dm-mapping:WHERE": {
                                "@foreignkey": "_foreign",
                                "@primarykey": "_poserr_148",
                            },
                        },
                    }
                ]
            },
        )
        self.assertDictEqual(
            builder.change_buffer["newcontent"][1],
            {
                "test.spectra": [
                    {
                        "dm-mapping:INSTANCE": {
                            "@dmrole": "test:spectrum",
                            "@dmtype": "test:Spectrum",
                            "dm-mapping:ATTRIBUTE": [
                                {
                                    "@dmrole": "test:spectrum.num",
                                    "@dmtype": "ivoa:string",
                                    "@ref": "_spc_148",
                                },
                                {
                                    "@dmrole": "test:spectrum.id",
                                    "@dmtype": "ivoa:real",
                                    "@ref": "_foreign",
                                },
                            ],
                        },
                        "dm-mapping:JOIN": {
                            "@tableref": "Spectra",
                            "dm-mapping:WHERE": {
                                "@foreignkey": "_foreign",
                                "@primarykey": "_poserr_148",
                            },
                        },
                    }
                ]
            },
        )

        builder = JsonMappingBuilder(json_dict=json_dict)
        builder.revert_collections()
        self.assertDictEqual(
            builder.json,
 {
  "dm-mapping:VODML": {
    "@xmlns:dm-mapping": "http://www.ivoa.net/xml/merged-syntax",
    "dm-mapping:GLOBALS": {
      "dm-mapping:INSTANCE": [
        {
          "@ID": "SpaceFrame_ICRS",
          "@dmtype": "coords:SpaceFrame",
          "dm-mapping:ATTRIBUTE": [
            {
              "@dmrole": "coords:SpaceFrame.spaceRefFrame",
              "@dmtype": "ivoa:string",
              "@value": "ICRS"
            },
            {
              "@dmrole": "coords:SpaceFrame.equinox",
              "@dmtype": "coords:Epoch",
              "@value": "NoSet"
            }
          ],
          "dm-mapping:INSTANCE": {
            "@dmrole": "coords:SpaceFrame.refPosition",
            "@dmtype": "coords:StdRefLocation",
            "dm-mapping:ATTRIBUTE": {
              "@dmrole": "coords:StdRefLocation.position",
              "@dmtype": "ivoa:string",
              "@value": "NoSet"
            }
          }
        },
        {
          "@dmrole": "root",
          "@dmtype": "test.model",
          "dm-mapping:INSTANCE": {
            "@dmrole": "test.header",
            "@dmtype": "test.Header",
            "dm-mapping:INSTANCE": {
              "@dmrole": "test.owner",
              "@dmtype": "test.Owner",
              "dm-mapping:ATTRIBUTE": [
                {
                  "@dmrole": "test.owner.name",
                  "@dmtype": "string",
                  "@value": "Michel"
                },
                {
                  "@dmrole": "test.owner.firstname",
                  "@dmtype": "string",
                  "@value": "Laurent"
                },
                {
                  "@dmrole": "test.title",
                  "@dmtype": "string",
                  "@ref": "_title"
                }
              ]
            },
            "dm-mapping:REFERENCE": {
              "@dmref": "SpaceFrame_ICRS",
              "@dmrole": "test.frame"
            },
            "test.points": [
              {
                "dm-mapping:JOIN": {
                  "@tableref": "Results"
                }
              }
            ]
          }
        }
      ]
    },
    "dm-mapping:MODEL": {
      "@name": "test"
    },
    "dm-mapping:TEMPLATES": [
      {
        "@tableref": "Results",
        "dm-mapping:INSTANCE": {
          "@ID": "_point",
          "@dmrole": "primary:point",
          "@dmtype": "Point",
          "dm-mapping:ATTRIBUTE": {
            "@dmrole": "test:detection.num",
            "@dmtype": "ivoa:real",
            "@ref": "_poserr_148"
          },
          "test.detections": [
            {
              "dm-mapping:INSTANCE": {
                "@dmrole": "test:detection",
                "@dmtype": "test:Detection",
                "dm-mapping:ATTRIBUTE": [
                  {
                    "@dmrole": "test:detection.num",
                    "@dmtype": "ivoa:real",
                    "@ref": "_num_148"
                  },
                  {
                    "@dmrole": "test:detection.id",
                    "@dmtype": "ivoa:real",
                    "@ref": "_foreign_other"
                  }
                ]
              },
              "dm-mapping:JOIN": {
                "@tableref": "OtherResults",
                "dm-mapping:WHERE": {
                  "@foreignkey": "_foreign_other",
                  "@primarykey": "_poserr_148"
                }
              }
            }
          ],
          "test.spectra": [
            {
              "dm-mapping:INSTANCE": {
                "@dmrole": "test:spectrum",
                "@dmtype": "test:Spectrum",
                "dm-mapping:ATTRIBUTE": [
                  {
                    "@dmrole": "test:spectrum.num",
                    "@dmtype": "ivoa:string",
                    "@ref": "_spc_148"
                  },
                  {
                    "@dmrole": "test:spectrum.id",
                    "@dmtype": "ivoa:real",
                    "@ref": "_foreign_spectra"
                  }
                ]
              },
              "dm-mapping:JOIN": {
                "@tableref": "Spectra",
                "dm-mapping:WHERE": {
                  "@foreignkey": "_foreign_spectra",
                  "@primarykey": "_poserr_148"
                }
              }
            }
          ]
        }
      },
      {
        "@tableref": "OtherResults",
        "dm-mapping:INSTANCE": {
          "@dmrole": "test:detection",
          "@dmtype": "test:Detection",
          "dm-mapping:ATTRIBUTE": [
            {
              "@dmrole": "test:detection.num",
              "@dmtype": "ivoa:real",
              "@ref": "_num_148"
            },
            {
              "@dmrole": "test:detection.id",
              "@dmtype": "ivoa:real",
              "@ref": "_foreign_other"
            }
          ]
        }
      },
      {
        "@tableref": "Spectra",
        "dm-mapping:INSTANCE": {
          "@dmrole": "test:spectrum",
          "@dmtype": "test:Spectrum",
          "dm-mapping:ATTRIBUTE": [
            {
              "@dmrole": "test:spectrum.num",
              "@dmtype": "ivoa:stringl",
              "@ref": "_spc_148"
            },
            {
              "@dmrole": "test:spectrum.id",
              "@dmtype": "ivoa:real",
              "@ref": "_foreign_spectra"
            }
          ]
        }
      }
    ]
  }
}
        )

    def test_revert_templates(self):
        builder = JsonMappingBuilder(
            json_dict={
                "dm-mapping:VODML": {
                    "@xmlns:dm-mapping": "http://www.ivoa.net/xml/merged-syntax",
                    "dm-mapping:GLOBALS": {},
                    "dm-mapping:MODEL": {"@name": "test"},
                },
                "dm-mapping:TEMPLATES": [
                    {
                        "@tableref": "Results",
                        "dm-mapping:INSTANCE": {
                            "@ID": "_point",
                            "@dmrole": "primary:point",
                            "@dmtype": "Point",
                            "dm-mapping:ATTRIBUTE": {
                                "@dmrole": "test:detection.num",
                                "@dmtype": "ivoa:real",
                                "@ref": "_poserr_148",
                            },
                            "dm-mapping:COLLECTION": [
                                {
                                    "@dmrole": "test.detections",
                                    "dm-mapping:INSTANCE": {
                                        "@dmrole": "test:detection",
                                        "@dmtype": "test:Detection",
                                        "dm-mapping:ATTRIBUTE": [
                                            {
                                                "@dmrole": "test:detection.num",
                                                "@dmtype": "ivoa:real",
                                                "@ref": "_num_148",
                                            },
                                            {
                                                "@dmrole": "test:detection.id",
                                                "@dmtype": "ivoa:real",
                                                "@ref": "_foreign",
                                            },
                                        ],
                                    },
                                    "dm-mapping:JOIN": {
                                        "@tableref": "OtherResults",
                                        "dm-mapping:WHERE": {
                                            "@foreignkey": "_foreign",
                                            "@primarykey": "_poserr_148",
                                        },
                                    },
                                },
                                {
                                    "@dmrole": "test.spectra",
                                    "dm-mapping:INSTANCE": {
                                        "@dmrole": "test:spectrum",
                                        "@dmtype": "test:Spectrum",
                                        "dm-mapping:ATTRIBUTE": [
                                            {
                                                "@dmrole": "test:spectrum.num",
                                                "@dmtype": "ivoa:string",
                                                "@ref": "_spc_148",
                                            },
                                            {
                                                "@dmrole": "test:spectrum.id",
                                                "@dmtype": "ivoa:real",
                                                "@ref": "_foreign",
                                            },
                                        ],
                                    },
                                    "dm-mapping:JOIN": {
                                        "@tableref": "Spectra",
                                        "dm-mapping:WHERE": {
                                            "@foreignkey": "_foreign",
                                            "@primarykey": "_poserr_148",
                                        },
                                    },
                                },
                            ],
                        },
                    }
                ],
            }
        )
        builder.revert_collections()

        builder.revert_templates()
        self.assertDictEqual(
            builder.json,
            {
                "dm-mapping:TEMPLATES": [
                    {
                        "@tableref": "Results",
                        "dm-mapping:INSTANCE": {
                            "@ID": "_point",
                            "@dmrole": "primary:point",
                            "@dmtype": "Point",
                            "dm-mapping:ATTRIBUTE": {
                                "@dmrole": "test:detection.num",
                                "@dmtype": "ivoa:real",
                                "@ref": "_poserr_148",
                            },
                            "dm-mapping:COLLECTION": [
                                {
                                    "@dmrole": "test.detections",
                                    "dm-mapping:INSTANCE": {
                                        "@dmrole": "test:detection",
                                        "@dmtype": "test:Detection",
                                        "dm-mapping:ATTRIBUTE": [
                                            {
                                                "@dmrole": "test:detection.num",
                                                "@dmtype": "ivoa:real",
                                                "@ref": "_num_148",
                                            },
                                            {
                                                "@dmrole": "test:detection.id",
                                                "@dmtype": "ivoa:real",
                                                "@ref": "_foreign",
                                            },
                                        ],
                                    },
                                    "dm-mapping:JOIN": {
                                        "@tableref": "OtherResults",
                                        "dm-mapping:WHERE": {
                                            "@foreignkey": "_foreign",
                                            "@primarykey": "_poserr_148",
                                        },
                                    },
                                },
                                {
                                    "@dmrole": "test.spectra",
                                    "dm-mapping:INSTANCE": {
                                        "@dmrole": "test:spectrum",
                                        "@dmtype": "test:Spectrum",
                                        "dm-mapping:ATTRIBUTE": [
                                            {
                                                "@dmrole": "test:spectrum.num",
                                                "@dmtype": "ivoa:string",
                                                "@ref": "_spc_148",
                                            },
                                            {
                                                "@dmrole": "test:spectrum.id",
                                                "@dmtype": "ivoa:real",
                                                "@ref": "_foreign",
                                            },
                                        ],
                                    },
                                    "dm-mapping:JOIN": {
                                        "@tableref": "Spectra",
                                        "dm-mapping:WHERE": {
                                            "@foreignkey": "_foreign",
                                            "@primarykey": "_poserr_148",
                                        },
                                    },
                                },
                            ],
                        },
                    }
                ],
                "dm-mapping:VODML": {
                    "@xmlns:dm-mapping": "http://www.ivoa.net/xml/merged-syntax",
                    "dm-mapping:GLOBALS": {},
                    "dm-mapping:MODEL": {"@name": "test"},
                    "dm-mapping:TEMPLATES": {},
                },
            },
        )

    def test_revert_elements(self):
        self.maxDiff = None
        jsonMappingBuilder = JsonMappingBuilder(
            json_dict={
                "dm-mapping:VODML": {
                    "@name": "MANGO",
                    "@syntax": "ModelInstanceInVot",
                    "dm-mapping:GLOBALS": {},
                    "dm-mapping:TEMPLATES": [
                        {"@tableref": "Results", "dm-mapping:COLLECTION": {}}
                    ],
                }
            }
        )
        jsonMappingBuilder.revert_elements("dm-mapping:TEMPLATES")
        self.assertDictEqual(
            jsonMappingBuilder.json,
            {
                "dm-mapping:VODML": {
                    "@name": "MANGO",
                    "@syntax": "ModelInstanceInVot",
                    "dm-mapping:GLOBALS": {},
                    "Results": [{"@tableref": "Results", "dm-mapping:COLLECTION": {}}],
                }
            },
        )
    """
    def test_all_reverts(self):
        self.maxDiff = None
        builder = JsonMappingBuilder(
            json_dict=DictUtils.read_dict_from_file(self.json_path)
        )
        
        
        builder.revert_collections()
        self.assertDictEqual(
            builder.json,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "./data/references/rich_instance_revert_coll.json"
                )
            ),
        )

        builder.revert_templates()
        self.assertDictEqual(
            builder.json,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "./data/references/rich_instance_revert_templ.json"
                )
            ),
        )

        builder.revert_elements("dm-mapping:INSTANCE")
        self.assertDictEqual(
            builder.json,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "./data/references/rich_instance_revert_inst.json"
                )
            ),
        )

        builder.revert_elements("dm-mapping:ATTRIBUTE")
        self.assertDictEqual(
            builder.json, DictUtils.read_dict_from_file(self.revert_json_path)
        )


    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/references/rich_instance_raw.json")
        self.revert_json_path = os.path.join(self.data_path, "./data/references/rich_instance_revert.json")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()