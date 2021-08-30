'''
Created on 20 avr. 2020

@author: laurentmichel
'''


class VodmlImport:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        retour = "IMPORT " + self.name + " " + self.url + "\n"
        return retour

    def __repr__(self):
        retour = "IMPORT " + self.name + " " + self.url + "\n"
        return retour
        
