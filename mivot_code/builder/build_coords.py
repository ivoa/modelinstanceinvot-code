'''
Created on 19 Jan 2023

@author: laurentmichel
'''
import os
from mivot_code.builder.builder2 import Builder

if __name__ == '__main__':
    for vodmlclass in ["PhysicalCoordinate", "LonLatPoint", "TimeStamp", "JD", "MJD", "SpaceSys", "TimeSys"]:

        builder = Builder(
            "coords",
            vodmlclass,
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "Coords-v1.0.vo-dml.xml"
                ),
                os.path.dirname(os.path.realpath(__file__))
            )
        builder.build()
    