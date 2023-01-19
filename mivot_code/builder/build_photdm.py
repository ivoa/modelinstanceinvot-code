'''
Created on 19 Jan 2023

@author: laurentmichel
'''
import os
from mivot_code.builder.builder2 import Builder

if __name__ == '__main__':
    for vodmlclass in ["PhotometryFilter", "PhotCal", "PhotometricSystem"]:
        builder = Builder(
            "Phot",
            vodmlclass,
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "Phot-v1.1.vodml.xml"
                ),
                os.path.dirname(os.path.realpath(__file__))
            )
        builder.build()
