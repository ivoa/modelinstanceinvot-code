'''
Apply the JSON mapping descriptor for the XMM catalog to the XMM VOTABLE 
Created on 15 avr. 2020

@author: laurentmichel
'''
import os, sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from product_annoter.demo import data_dir
  
from product_annoter.mapper.product_mapper import ProductMapper    
if __name__ == '__main__':
        base_path = os.path.dirname(os.path.realpath(__file__)) 
        
        productMapper = ProductMapper(data_dir,
                                          "vizier_grouped_col")
        productMapper.build_annotations()
