'''
Created on 19 Jan 2023

@author: laurentmichel
'''
import os
from mivot_code.builder.builder2 import Builder

if __name__ == '__main__':
    for vodmlclass in ["Position", "Velocity", "ProperMotion", "Time", 
                       'GenericMeasure', "Symmetrical", 
                       "Asymmetrical1D", "Asymmetrical2D",
                       "Ellipse"]:
        builder = Builder(
            "meas",
            vodmlclass,
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "Meas-v1.vo-dml.xml"
                ),
                os.path.dirname(os.path.realpath(__file__))
            )
        builder.build()
