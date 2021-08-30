'''
Created on Feb 26, 2021

@author: laurentmichel
'''
import unittest
import os
from client.tests import logger
from client.translator.json_mapping_builder import JsonMappingBuilder
from utils.dict_utils import DictUtils

class Test(unittest.TestCase):


    def test__revert_composition(self):
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {
                        "@dmrole": "collection.content"
                    }
                   }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder._revert_composition( jsonMappingBuilder.json['MODEL_INSTANCE'],  "COLLECTION")
        self.assertDictEqual(jsonMappingBuilder.change_buffer, 
            {
              "newcontent": [
                {
                  "collection.content": []
                }
              ],
              "node": {
                "@tableref": "Results",
                "COLLECTION": {
                  "@dmrole": "collection.content"
                }
              }
            }        
            )        
        
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": [{
                        "@dmrole": "collection.content"
                    }]
                   }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder._revert_composition( jsonMappingBuilder.json['MODEL_INSTANCE'],  "COLLECTION")
        self.assertDictEqual(jsonMappingBuilder.change_buffer, 
            {
              "newcontent": [
                {
                  "collection.content": []
                }
              ],
              "node": {
                "@tableref": "Results",
                "COLLECTION": [
                    {
                        "@dmrole": "collection.content"
                    }
                ]
              }
            }        
        )
        
        
    def test_revert_compositions(self):
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {
                        "@dmrole": "collection.content"
                    }
                   }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder.revert_compositions("COLLECTION")
        print(DictUtils.get_pretty_json(jsonMappingBuilder.json))

        self.assertDictEqual(jsonMappingBuilder.json, 
                {
                  "MODEL_INSTANCE": {
                    "@name": "MANGO",
                    "@syntax": "ModelInstanceInVot",
                    "GLOBALS": {},
                    "TABLE_MAPPING": [
                      {
                        "@tableref": "Results",
                        "collection.content": []
                      }
                    ]
                  }
                }
            )        
        
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": [{
                        "@dmrole": "collection.content"
                    }]
                   }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder._revert_composition( jsonMappingBuilder.json['MODEL_INSTANCE'],  "COLLECTION")
        print(DictUtils.get_pretty_json(jsonMappingBuilder.change_buffer))
        self.assertDictEqual(jsonMappingBuilder.change_buffer, 
            {
              "newcontent": [
                {
                  "collection.content": []
                }
              ],
              "node": {
                "@tableref": "Results",
                "COLLECTION": [
                    {
                        "@dmrole": "collection.content"
                    }
                ]
              }
            }        
        )
        
    def test__revert_subelement(self):
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {
                    }
                   }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder._revert_subelement( jsonMappingBuilder.json['MODEL_INSTANCE'],  "TABLE_MAPPING")

        self.assertDictEqual(jsonMappingBuilder.change_buffer, 
            {
              "newcontent": {
                "Results": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {}
                  }
                ]
              },
              "node": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {}
                  }
                ]
              }
            }
        )
        
        
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
                [
                  {
                      "TABLE_MAPPING": [
                          {
                            "@tableref": "Results",
                            "COLLECTION": {}
                          }
                      ]                   
                    }
                ]
        )                                                 
        jsonMappingBuilder._revert_subelement( jsonMappingBuilder.json,  "TABLE_MAPPING")
        self.assertDictEqual(jsonMappingBuilder.change_buffer, 
                {
                  "newcontent": {
                    "Results": [
                      {
                        "@tableref": "Results",
                        "COLLECTION": {}
                      }
                    ]
                  },
                  "node": {
                    "TABLE_MAPPING": [
                      {
                        "@tableref": "Results",
                        "COLLECTION": {}
                      }
                    ]
                  }
                }
        )
        
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
                [
                  {
                      "TABLE_MAPPING": [
                          {
                            "@tableref": "Results",
                            "COLLECTION": {}
                          }
                      ]                   
                    },
                  {
                      "TABLE_MAPPING": [
                          {
                            "@tableref": "Results2",
                            "COLLECTION": {}
                          }
                      ]                   
                    }
                ]
        )                                                 
        jsonMappingBuilder._revert_subelement( jsonMappingBuilder.json,  "TABLE_MAPPING")
        self.assertDictEqual(jsonMappingBuilder.change_buffer, 
                {
                  "newcontent": {
                    "Results": [
                      {
                        "@tableref": "Results",
                        "COLLECTION": {}
                      }
                    ]
                  },
                  "node": {
                    "TABLE_MAPPING": [
                      {
                        "@tableref": "Results",
                        "COLLECTION": {}
                      }
                    ]
                  }
                }
        )
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {  
                "TABLE_MAPPING":  {
                    "@tableref": "Results",
                    "COLLECTION": {}
                 }
            }
                
                  
        )                                                 
        jsonMappingBuilder._revert_subelement( jsonMappingBuilder.json,  "TABLE_MAPPING")
        self.assertDictEqual(jsonMappingBuilder.change_buffer, 
            {
              "newcontent": {
                "Results": {
                  "@tableref": "Results",
                  "COLLECTION": {}
                }
              },
              "node": {
                "TABLE_MAPPING": {
                  "@tableref": "Results",
                  "COLLECTION": {}
                }
              }
            }
        )
        
    def test_revert_elements(self):
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {
                    }
                   }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder.revert_elements("TABLE_MAPPING")
        self.assertDictEqual(jsonMappingBuilder.json, 
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "Results": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {}
                  }
                ]
              }
            }       
        )
        

        
    """

    def test_revert_elements(self):
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {
                    }
                    }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder.revert_elements("TABLE_MAPPING")
        print(DictUtils.get_pretty_json(jsonMappingBuilder.retour))
        print(DictUtils.get_pretty_json(jsonMappingBuilder.json))

        self.assertDictEqual(jsonMappingBuilder.retour, 
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": {
                  "Results": [
                    {
                      "@tableref": "Results",
                      "COLLECTION": {}
                    }
                  ]
                }
              }
            }
        )
       
    """
    """ 
    def test_revert_templates(self):
        jsonMappingBuilder  = JsonMappingBuilder(json_dict=
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": [
                  {
                    "@tableref": "Results",
                    "COLLECTION": {
                    }
                    }
                ]
            }
          }
        )                                                 
        jsonMappingBuilder.revert_templates()
        self.assertDictEqual(jsonMappingBuilder.json, 
            {
              "MODEL_INSTANCE": {
                "@name": "MANGO",
                "@syntax": "ModelInstanceInVot",
                "GLOBALS": {},
                "TABLE_MAPPING": {
                  "Results": [
                    {
                      "@tableref": "Results",
                      "COLLECTION": {}
                    }
                  ]
                }
              }
            }
                             )
    """

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_json_mapping_builder.json")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()