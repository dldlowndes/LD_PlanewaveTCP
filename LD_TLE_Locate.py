import LD_TLETool
import sgp4.api
import astropy
import astropy.coordinates
import astropy.time
import astropy.units

datetime_Now = astropy.time.Time.now()

tle_List = LD_TLETool.TLE_List("active.txt", False)
my_tle_str = tle_List.Get_TLE_String(tle_List.Search_Keys("zarya"))
tle = LD_TLETool.My_TLE(my_tle_str)

sat = sgp4.api.Satrec.twoline2rv(tle[1], tle[2])
e, p, v = sat.sgp4(datetime_Now.jd, 0)

teme_p = astropy.coordinates.CartesianRepresentation(p * astropy.units.km)
teme_v = astropy.coordinates.CartesianDifferential(v * (astropy.units.km / astropy.units.s))

# see https://docs.astropy.org/en/latest/coordinates/satellites.html
# but needs >=astropy4.1 (which anaconda hasn't caught up to yet)
teme = astropy.coordinates.TEME(teme_p.with_differentials(teme_v), obstime = datetime_Now.jd)