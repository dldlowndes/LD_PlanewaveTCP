import astropy
import astropy.coordinates
import astropy.time
import datetime
import dateutil
import pytz

import matplotlib.pyplot as plt

class PassFinder:
    def __init__(self, my_tle, lat, long, height):
        self.my_tle = my_tle

        # Turn the current location into astropy coordinates (and then at a specific time)
        self.here = astropy.coordinates.EarthLocation(lat=lat, lon=long, height=height * astropy.units.m)


    def _Get_Coords(self, m_obstime):
        sat = sgp4.api.Satrec.twoline2rv(self.my_tle[1], self.my_tle[2])
        e, p, v = sat.sgp4(m_obstime.jd, 0)

        # SGP4 gives results in some weird coordinate basis (True Equator Mean Equinox frame (TEME))
        # Get values in the right format to convert to something more intelligible and useful.
        teme_p = astropy.coordinates.CartesianRepresentation(p * astropy.units.km)
        teme_v = astropy.coordinates.CartesianDifferential(v * (astropy.units.km / astropy.units.s))

        # Put the coordinates into astropy so it can convert (then convert)
        # International Terrestrial Reference System (ITRS) makes sense.
        teme = astropy.coordinates.TEME(teme_p.with_differentials(teme_v), obstime = m_obstime)
        itrs = teme.transform_to(astropy.coordinates.ITRS(obstime=m_obstime))
        return itrs

        #location = itrs.earth_location
        #return location.geodetic

    def Get_AltAz(self, iso_Datetime = None):
        if iso_Datetime is None:
            datetime_Now = astropy.time.Time.now()
            m_obstime = astropy.time.Time(datetime_Now)
        else:
            m_obstime = astropy.time.Time(iso_Datetime)
        #print(f"Time is {m_obstime}")

        sat_coords = self._Get_Coords(m_obstime)

        # observer is a location (here) at a time (datetime_now) (since the earth is moving)
        observer = astropy.coordinates.AltAz(location=self.here, obstime=m_obstime)
        # Get the coordinates of the satelite as seen from the observer
        view = sat_coords.transform_to(observer)

        return view.alt, view.az


if __name__ == "__main__":
    my_tles = TLE_List("active.txt", False)
    sat_key = my_tles.Search_Keys("resurs-dk")
    tle = my_tles.tle_Dict[sat_key]
    satellite = My_TLE(tle)

    find = PassFinder(satellite, 51.456671, -2.601768, 71)

    t0 = datetime.datetime.strptime("2020-05-31T21:00:00", "%Y-%m-%dT%H:%M:%S")
    tx = datetime.datetime.strptime("2020-06-01T05:00:00", "%Y-%m-%dT%H:%M:%S")
    ti = datetime.timedelta(minutes=1)
    altazes = []
    while t0 <= tx:
        time_str = str(datetime.datetime.utcfromtimestamp(t0.timestamp()))
        alt, az = find.Get_AltAz(time_str)
        print(time_str, alt.degree, az.degree)
        altazes.append([t0.timestamp(), alt.degree, az.degree])
        t0 = t0 + ti

    aa = np.array(altazes)
    plt.plot(aa[:,0], aa[:,1])