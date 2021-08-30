'''
Created on Feb 26, 2021

@author: laurentmichel
'''
import unittest
from client.inst_builder.json_block_extractor import JsonBlockExtractor
from utils.dict_utils import DictUtils

class Test(unittest.TestCase):

    def test__search_array_container_1(self):
        jsonBlockExtractor  = JsonBlockExtractor(
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
        jsonBlockExtractor._search_array_container("COLLECTION", jsonBlockExtractor.json_block)
        self.assertListEqual(jsonBlockExtractor.searched_elements, 
                [
                  [
                    {
                      "@tableref": "Results",
                      "COLLECTION": {
                        "@dmrole": "collection.content"
                      }
                    }
                  ]
                ]             
                , "")
        
    def test__search_array_container_2(self):
        jsonBlockExtractor  = JsonBlockExtractor(
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
                   },
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
        jsonBlockExtractor._search_array_container("COLLECTION", jsonBlockExtractor.json_block)

        self.assertListEqual(jsonBlockExtractor.searched_elements, 
                [
                  [
                    {
                      "@tableref": "Results",
                      "COLLECTION": {
                        "@dmrole": "collection.content"
                      }
                    },
                    {
                      "@tableref": "Results",
                      "COLLECTION": {
                        "@dmrole": "collection.content"
                      }
                    }
                  ]
                ]                , "")

    def test__search_array_container_3(self):
        jsonBlockExtractor = JsonBlockExtractor(
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
                ],
                "TABLE_MAPPING_2": [
                  {
                    "@tableref": "Results2",
                    "COLLECTION": {
                        "@dmrole": "collection2.content"
                    }
                   }
                ]

            }
          }
        )                                                 
        jsonBlockExtractor._search_array_container("COLLECTION", jsonBlockExtractor.json_block)
        #print(DictUtils.get_pretty_json(jsonBlockExtractor.searched_elements))
        self.assertListEqual(jsonBlockExtractor.searched_elements, 
            [
              [
                {
                  "@tableref": "Results",
                  "COLLECTION": {
                    "@dmrole": "collection.content"
                  }
                }
              ],
              [
                {
                  "@tableref": "Results2",
                  "COLLECTION": {
                    "@dmrole": "collection2.content"
                  }
                }
              ]
            ]                , "")
        
        
    def test__search_array_container_4(self):
        jsonBlockExtractor  = JsonBlockExtractor(
            [{
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
          }]
        )                                                 
        jsonBlockExtractor._search_array_container("COLLECTION", jsonBlockExtractor.json_block)
        self.assertListEqual(jsonBlockExtractor.searched_elements, 
                [
                  [
                    {
                      "@tableref": "Results",
                      "COLLECTION": {
                        "@dmrole": "collection.content"
                      }
                    }
                  ]
                ]             
                , "")
 
    def test__search_array_container_5(self):
        jsonBlockExtractor  = JsonBlockExtractor(
            [{
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
          }]
        )                                                 
        jsonBlockExtractor._search_array_container("COLLECTION", jsonBlockExtractor.json_block)
        self.assertListEqual(jsonBlockExtractor.searched_elements, 
                [
                  [
                    {
                      "@tableref": "Results",
                      "COLLECTION": {
                        "@dmrole": "collection.content"
                      }
                    }
                  ]
                ]             
                , "")
        
    def test__search_array_container_6(self):
        
        jsonBlockExtractor = JsonBlockExtractor(
           [ {
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
                ],
                "TABLE_MAPPING_2": [
                  {
                    "@tableref": "Results2",
                    "COLLECTION": {
                        "@dmrole": "collection2.content"
                    }
                   }
                ]

            }
          }]
        )                                                 
        jsonBlockExtractor._search_array_container("COLLECTION", jsonBlockExtractor.json_block)
        #print(DictUtils.get_pretty_json(jsonBlockExtractor.searched_elements))
        self.assertListEqual(jsonBlockExtractor.searched_elements, 
            [
              [
                {
                  "@tableref": "Results",
                  "COLLECTION": {
                    "@dmrole": "collection.content"
                  }
                }
              ],
              [
                {
                  "@tableref": "Results2",
                  "COLLECTION": {
                    "@dmrole": "collection2.content"
                  }
                }
              ]
            ]                , "")
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()