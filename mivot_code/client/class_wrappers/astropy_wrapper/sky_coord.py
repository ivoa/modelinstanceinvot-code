"""
Created on 27 Jan 2022
@author: laurentmichel
"""
import astropy.coordinates as coord
import astropy.units as u
from mivot_code.client.xml_interpreter.exceptions import NotImplementedException

class SkyCoord(object):
    '''
    Astropy wrapper
    Starting from a list of Meas instances, it builds the most possible complete SkyCoord instance
    
    WATCHOUT: this is proof of concept well suited for the project examples
              it is not intended to be used in a wider scope
    '''


    def __init__(self, stc_measures):
        '''
        Constructor
        '''
        self.stc_measures = stc_measures
        self.position = []
        self.frame = None
        self.pm_ra = None
        self.pm_dec = None
        self.distance = None
        self.radial_velocity = None
        self._set_position()
        self._set_proper_motion()
        self._set_distance()
        self._set_radial_velocity()

    """
    Private methods
    """

    def _set_position(self):
        """
        Look for the STC Position component (with its frame)
        """
        for stc_measure in self.stc_measures:
            if stc_measure.ucd == "pos":
                ra = stc_measure.coord.lon.value
                dec = stc_measure.coord.lat.value
                if stc_measure.coord.lon.unit != "deg":
                    raise NotImplementedException(f"ra dec unit {stc_measure.coord.lon.unit} not supported")
                self.position = [ra*u.deg, dec*u.deg]
                if stc_measure.coord.coordSys.dmtype != "ICRS":
                    raise NotImplementedException(f"space frame {stc_measure.coord.coordSys.dmtype} not supported")
                self.frame = "icrs"
                return

    def _set_proper_motion(self):
        """
        Look for the STC Proper motion component
        """
        for stc_measure in self.stc_measures:
            if stc_measure.ucd == "pos.pm":
                if stc_measure.coord.lon.unit != "mas/year":
                    raise NotImplementedException(f"proper motion unit {stc_measure.coord.lon.unit} not supported")
                self.pm_ra = stc_measure.coord.lon.value*u.mas/u.yr
                self.pm_dec = stc_measure.coord.lat.value*u.mas/u.yr
                return

    def _set_distance(self):
        """
        Look for a parallax GenericMeasure to be used to compute the distance
        """
        for stc_measure in self.stc_measures:
            if stc_measure.ucd == "pos.parallax":
                if stc_measure.coord.cval.unit != "mas":
                    raise NotImplementedException(f"parallax unit {stc_measure.coord.cval.unit} not supported")
                self.distance = abs(stc_measure.coord.cval.value*u.mas).to(u.pc, u.parallax())
                return

    def _set_radial_velocity(self):
        """
        Look for the STC Proper motion component
        """
        for stc_measure in self.stc_measures:
            if stc_measure.ucd == "spect.dopplerVeloc.opt":
                if stc_measure.coord.dist.unit != "km/s":
                    raise NotImplementedException(f"radial velocity unit {stc_measure.coord.dist.unit} not supported")
                self.radial_velocity = stc_measure.coord.dist.value*u.km/u.s
                return

    """
    Public interface methods
    """
    def get_sky_coord(self):
        """
        Try to build an Astropy.SkyCoord instance with the available parameters 
        """
        # Make sure to have a valid object or None
        if not self.position or self.frame is None:
            return None
        return coord.SkyCoord(ra=self.position[0], dec=self.position[1],
                    distance=self.distance,
                    pm_ra_cosdec=self.pm_ra,
                    pm_dec=self.pm_dec,
                    radial_velocity=self.radial_velocity,
                    frame=self.frame)