import requests

import LD_PWI_Status

# TODO:
#   - Separate classes for "model", "focuser", "rotator" etc? (or just lump together?)
#   - Handle errors gracefully
#   - Break out the status into a class so it can have typed data and get/set methods
#   - Some option to enable/disable single axes (should both axes be default though?)
#   - Get some documentation about these functions (email sent, awaiting reply)

class PWI_Device():
    """
    Base class for aspects of the Planewave telescope system that communicates
    via the PWI4 software (by GET requests to an HTTP server run by PWI4)

    ip_Address is usually localhost (http://127.0.0.1) and must have the http
    at the beginning.

    port is defined in the software (mine says 8220)
    """

    def __init__(self, ip_Address, port):
        self.base_Url = ":".join([ip_Address, port])

        # Dictionary containing the status message of the device.
        self.status = LD_PWI_Status.PWI_Status()

    def _SendMsg(self, command, **kwargs):
        """
        Makes GET requests to the PWI4 server. The commands are to specific
        URLs (such as "127.0.0.1:8220/mount/enable" for commands that need no
        parameters or use the query string "?" to add parameters separated by
        "&") - this is all dealt with by the requests package.

        Parameters are passed in as a dictionary to this function and passed
        straight to requests.get().
        """

        # Make the URL for the command (not including any params)
        cmd_Url = "/".join([self.base_Url, *command])

        # Make the GET request including the parameters (if present)
        response = requests.get(cmd_Url, kwargs)

        # Interpret response or complain it failed.
        if response.status_code == 200:
            self.status.Update(response)
        else:
            print(f"Response code {response.status_code}")
            print(f"{response.reason}")
            print(f"Request was {response.url}")

    
class Planewave_Mount(PWI_Device):
    """
    Interface to the telescope mount controlled by the PWI4 software.
    Currently only the mount is supported (ie not the focusser etc)
    """

    def __init__(self, ip_Addr="http://127.0.0.1", port="8220"):
        super().__init__(ip_Addr, port)

    def Connect(self):
        self._SendMsg(["mount", "connect"])

    def Disconnect(self):
        self._SendMsg(["mount", "disconnect"])

    def Enable(self):
        """
        Enable both axes at once.
        """
        for axis_Number in [0, 1]:
            self._SendMsg(["mount", "enable"], axis=axis_Number)

    def Disable(self):
        """
        Disable both axes at once.
        """
        for axis_Number in [0, 1]:
            self._SendMsg(["mount", "disable"], axis=axis_Number)

    def Status(self):
        """
        Get the full status.
        """
        self._SendMsg(["status"])

        return self._status

    def Home(self):
        self._SendMsg(["mount", "find_home"])

    def Stop(self):
        self._SendMsg(["mount", "stop"])

    def Goto_RaDec_Apparent(self, ra_Hours, dec_Degrees):
        self._SendMsg(["mount", "goto_ra_dec_apparent"],
                      ra_hours=ra_Hours,
                      dec_degs=dec_Degrees)

    def Goto_RaDec_J2000(self, ra_Hours, dec_Degrees):
        self._SendMsg(["mount", "goto_ra_dec_j2000"],
                      ra_hours=ra_Hours,
                      dec_degs=dec_Degrees)

    def Goto_AltAz(self, alt_Degrees, az_Degrees):
        self._SendMsg(["mount", "goto_alt_az"],
                      alt_degs=alt_Degrees,
                      az_degs=az_Degrees)

    def Mount_Offset(self):
        """
        One or more of the following offsets can be specified as a keyword argument:

        AXIS_reset: Clear all position and rate offsets for this axis. Set this to any value to issue the command.
        AXIS_stop_rate: Set any active offset rate to zero. Set this to any value to issue the command.
        AXIS_add_arcsec: Increase the current position offset by the specified amount
        AXIS_set_rate_arcsec_per_sec: Continually increase the offset at the specified rate

        Where AXIS can be one of:

        ra: Offset the target Right Ascension coordinate
        dec: Offset the target Declination coordinate
        axis0: Offset the mount's primary axis position
               (roughly Azimuth on an Alt-Az mount, or RA on In equatorial mount)
        axis1: Offset the mount's secondary axis position
               (roughly Altitude on an Alt-Az mount, or Dec on an equatorial mount)
        path: Offset along the direction of travel for a moving target
        transverse: Offset perpendicular to the direction of travel for a moving target

        For example, to offset axis0 by -30 arcseconds and have it continually increase at 1
        arcsec/sec, and to also clear any existing offset in the transverse direction,
        you could call the method like this:

        mount_offset(axis0_add_arcsec=-30, axis0_set_rate_arcsec_per_sec=1, transverse_reset=0)

        """
        raise NotImplementedError

    def Park(self):
        self._SendMsg(["mount", "park"])

    def Park_Here(self):
        self._SendMsg(["mount", "set_park_here"])

    def Tracking_On(self):
        self._SendMsg(["mount", "tracking_on"])

    def Tracking_Off(self):
        self._SendMsg(["mount", "tracking_off"])

    def Follow_TLE(self, tle_Lines):
        assert len(tle_Lines) == 3 # todo: more validation of tles
        self._SendMsg(["mount", "follow_tle"],
                      line1=tle_Lines[0],
                      line2=tle_Lines[1],
                      line3=tle_Lines[2])


if __name__ == "__main__":
    myMount = Planewave_Mount("http://192.168.1.170", "8220")
    myMount.Connect()
    myMount.Goto_RaDec_Apparent(10, 10)