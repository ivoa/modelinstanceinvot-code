'''
Created on 25 Jan 2022

@author: laurentmichel
'''

class QuantityConverter(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    @staticmethod
    def parallax_to_distance(parallax):
        """
        Parallax given in mas
        distance returned in parsec
        """
        # https://edu.obs-mip.fr/la-parallaxe-grace-au-satellite-gaia/
        if parallax == 0:
            return float('Inf')
        elif parallax < 0 :
            return -1/(parallax/1000.)
        else:
            return 1/(parallax/1000.)
