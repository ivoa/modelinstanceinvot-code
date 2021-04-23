'''
Created on 6 avr. 2020

@author: laurentmichel
'''
from astropy.coordinates import Galactic, ICRS, FK5, FK4, EarthLocation
from astropy.time import Time


class AstropyWrapper(object):
    '''
    classdocs
    '''

    def __init__(self, vodml_instance, mapper_name):
        '''
        Constructor
        '''
        self.vodml_instance = vodml_instance
        self.table_mapper = vodml_instance.table_mappers[mapper_name]
    
    def get_space_frame(self, element):
            # ref_location = self.table_mapper.search_instance_by_role("coords:StdRefLocation.position", 
            #                                                root_element=ele)[0]['@value']
            # print(ref_location)               
            frame_instance = self.table_mapper.search_instance_by_type("coords:SpaceFrame",
                                                            root_element=element)[0]
                                                            
            ref_frame = self.table_mapper.search_instance_by_role("coords:SpaceFrame.spaceRefFrame",
                                                            root_element=frame_instance)[0]['@value'].upper()  
            if ref_frame == "Galactic":
                retour = Galactic()
            elif ref_frame == "ICRS":
                retour = ICRS()
            else :
                ref_equinox = self.table_mapper.search_instance_by_role("coords:SpaceFrame.equinox",
                                                            root_element=frame_instance)[0]['@value'] 
                         
                if ref_frame == "FK4":
                    if not ref_equinox :
                        retour = FK4()
                    else:
                        retour = FK4(equinox=ref_equinox)

                elif ref_frame == "FK5":
                    if not ref_equinox :
                        retour = FK5()
                    else:
                        retour = FK5(equinox=ref_equinox)
                else:
                    raise Exception ("unsupported frame: " + ref_frame)    
            return retour   
        
    def get_time_frame(self, element):
            # ref_location = self.table_mapper.search_instance_by_role("coords:StdRefLocation.position", 
            #                                                root_element=ele)[0]['@value']
            # print(ref_location)               
            frame_instance = self.table_mapper.search_instance_by_type("coords:TimeFrame",
                                                            root_element=element)[0]
            ref_position_block = frame_instance["coords:TimeFrame.refPosition"]                                           
            ref_scale = self.table_mapper.search_instance_by_role(
                "coords:StdRefLocation.position",
                root_element=ref_position_block)[0]['@value'].upper()  
            ref_location = None
            if  "coords:TimeFrame.refLocation" in frame_instance:
                ref_location_block = frame_instance["coords:TimeFrame.refLocation"]
                ref_location = self.table_mapper.search_instance_by_role(
                    "coords:StdRefLocation.position",
                    root_element=ref_location_block)[0]['@value'].upper() 
                 
            if ref_scale == "BARYCENTER":
                ref_scale = "tcb"   
            if ref_location == "GEOCENTRIC":
                ref_location = EarthLocation.from_geocentric(0, 0, 0, 'm') 
                                                                            
            astrotime = Time(50000., scale=ref_scale, format='mjd', location=ref_location)    
            return astrotime.scale, astrotime.location, astrotime.format                                
                                                            
    
