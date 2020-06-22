import logging
import requests
import sys

import LD_PWI_Status

import LD_MyTLE

log = logging.getLogger(__name__)
url_Log = logging.getLogger("urllib3")
url_Log.setLevel(logging.WARNING)

class LD_Planewave:
    """
    Interface to the telescope mount controlled by the PWI4 software.
    Currently only the mount is supported (ie not the focusser etc)
    """

    def __init__(self, ip_Address="", port=""):

        if ip_Address != "":
            log.debug(f"Connecting to {ip_Address}:{port}")
            self.Connect_IP(ip_Address, port)
        else:
            log.warning("No IP address supplied (yet). Use Connect_IP(ip, port) later")

    def Connect_IP(self, ip_Address="http://127.0.0.1", port="8220"):
        self.base_Url = f"{ip_Address}:{port}"

        # Container for the status messages of the device.
        self.status = LD_PWI_Status.LD_PWI_Status()

    def _SendMsg(self, command, **kwargs):
        """
        Makes GET requests to the PWI4 server. The commands are to specific
        URLs (such as "127.0.0.1:8220/mount/enable" for commands that need no
        parameters or use the query string "?" to add parameters separated by
        "&") - this is all dealt with by the requests package.

        Parameters are passed in as a dictionary to this function and passed
        straight to requests.get().
        """

        if isinstance(command, (list, tuple)):
            # Make the URL for the command (not including any params)
            cmd_Url = "/".join([self.base_Url, *command])
        elif isinstance(command, str):
            # If a string was passed, interpret it as a direct command.
            cmd_Url = f"{self.base_Url}/{command}"
            log.debug("Direct command {cmd_url}")
        else:
            cmd_Url = ""
            log.warning("Don't know how to interpret {command} of type {type(command)}")

        # Make the GET request including the parameters (if present)
        response = requests.get(cmd_Url, kwargs)

        # Interpret response or complain it failed.
        if response.status_code == 200:
            self.status.Update(response)
        else:
            log.warning(f"Response code {response.status_code}")
            log.warning(f"{response.reason}: {response.content}")
            log.warning(f"Request was {response.url}")

        return response

    def Connect(self):
        """
        Connect to the telescope hardware.
        """
        log.debug("Connect to telescope hardware")
        response = self._SendMsg(["mount", "connect"])
        log.debug(f"Telescope says {response}")
        return response

    def Disconnect(self):
        """
        Disconnect from the telescope hardware.
        """
        log.debug("Disconnect from telescope hardware")
        response = self._SendMsg(["mount", "disconnect"])
        log.debug(f"Telescope says {response}")
        return response

    def Enable(self, axis):
        """
        Enable chosen axis
        """
        return self._SendMsg(["mount", "enable"], axis=axis)

    def Disable(self, axis):
        """
        Disable chosen axis
        """
        response = self._SendMsg(["mount", "disable"], axis=axis)
        log.debug(f"Telescope says {response}")
        return response

    def Status(self):
        """
        Get the full status.
        """
        response = self._SendMsg(["status"])

        return self.status

    def Home(self):
        log.debug("Home mount")
        response = self._SendMsg(["mount", "find_home"])
        log.debug(f"Telescope says {response}")
        return response

    def Stop(self):
        log.debug("Stop mount")
        response = self._SendMsg(["mount", "stop"])
        log.debug(f"Telescope says {response}")
        return response

    def Goto_RaDec_Apparent(self, ra_Hours, dec_Degrees):
        log.debug(f"Go do ra/dec (apparent) {ra_Hours}h, {dec_Degrees}deg")
        response = self._SendMsg(["mount", "goto_ra_dec_apparent"],
                                 ra_hours=ra_Hours,
                                 dec_degs=dec_Degrees)
        log.debug(f"Telescope says {response}")
        return response

    def Goto_RaDec_J2000(self, ra_Hours, dec_Degrees):
        log.debug(f"Go do ra/dec (J2000) {ra_Hours}h, {dec_Degrees}deg")
        response = self._SendMsg(["mount", "goto_ra_dec_j2000"],
                                 ra_hours=ra_Hours,
                                 dec_degs=dec_Degrees)
        log.debug(f"Telescope says {response}")
        return response

    def Goto_AltAz(self, alt_Degrees, az_Degrees):
        log.debug(f"Go do alt/az {alt_Degrees}deg alt, {az_Degrees}deg az")
        response = self._SendMsg(["mount", "goto_alt_az"],
                                 alt_degs=alt_Degrees,
                                 az_degs=az_Degrees)
        log.debug(f"Telescope says {response}")
        return response

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
        log.debug("Park mount")
        response = self._SendMsg(["mount", "park"])
        log.debug(f"Telescope says {response}")
        return response

    def Park_Here(self):
        log.debug("Park mount here")
        response = self._SendMsg(["mount", "set_park_here"])
        log.debug(f"Telescope says {response}")
        return response

    def Tracking_On(self):
        log.debug("Mount track on")
        response = self._SendMsg(["mount", "tracking_on"])
        log.debug(f"Telescope says {response}")
        return response

    def Tracking_Off(self):
        log.debug("Mount track off")
        response = self._SendMsg(["mount", "tracking_off"])
        log.debug(f"Telescope says {response}")
        return response

    def Follow_TLE(self, tle):
        """
        Instruct the mount to follow a TLE. Argument tle can either be:
            str: a raw string of the whole TLE, separated by "\n" etc.
            list: a list with a string for each line of the TLE.
            dict: a dict with keys line0, line1, line2 holding strings for each line of TLE
            My_TLE: An instance of my TLE class
        """

        if isinstance(tle, str):
            tle = tle.split("\n")
        if isinstance(tle, list):
            assert len(tle) == 3
            tle_Payload = {
                "line0": tle[0],
                "line1": tle[1],
                "line2": tle[2]
                }
        elif isinstance(tle, dict):
            tle_Payload = tle
        elif isinstance(tle, LD_MyTLE.LD_MyTLE):
            tle_Payload = tle.Dict

        log.debug(f"Follow TLE named {tle_Payload['line0']}")

        response = self._SendMsg(["mount", "follow_tle"],
                                 **tle_Payload
                                 )
        log.debug(f"Telescope says {response}")
        return response

    def Raw_Command(self, raw_Str):
        """
        Allow (an advanced?) user to speficy some exact raw command to the
        mount. (i.e.) a specific HTTP request and return the response.
        """
        
        if isinstance(raw_Str, str):
            response = self._SendMsg(raw_Str)
            return response
        else:
            log.warning("Raw commands can only be strings")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    myMount = LD_Planewave("http://127.0.0.1", "8220")
    myMount.Connect()
    print(myMount.status)

    myMount.Tracking_On()

    print("Request TLE")
    iss_TLE = ["ISS (ZARYA)",
               "1 25544U 98067A   20140.34419374 -.00000374  00000-0  13653-5 0  9990",
               "2 25544  51.6433 131.2277 0001338 330.3524 173.1622 15.49372617227549"
               ]
    r = myMount.Follow_TLE(iss_TLE)
