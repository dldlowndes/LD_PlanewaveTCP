try:
    # Python 3.x version
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    # Python 2.7 version
    from urllib import urlencode
    from urllib2 import urlopen, HTTPError

class PWI4:
    """
    Client to the PWI4 telescope control application.
    """

    def __init__(self, host="localhost", port=8220):
        self.host = host
        self.port = port
        self.comm = PWI4HttpCommunicator(host, port)

    ### High-level methods #################################

    def status(self):
        return self.request_with_status("/status")

    def mount_connect(self):
        return self.request_with_status("/mount/connect")

    def mount_disconnect(self):
        return self.request_with_status("/mount/disconnect")

    def mount_enable(self, axisNum):
        return self.request_with_status("/mount/enable", axis=axisNum)

    def mount_disable(self, axisNum):
        return self.request_with_status("/mount/disable", axis=axisNum)

    def mount_find_home(self):
        return self.request_with_status("/mount/find_home")

    def mount_stop(self):
        return self.request_with_status("/mount/stop")

    def mount_goto_ra_dec_apparent(self, ra_hours, dec_degs):
        return self.request_with_status("/mount/goto_ra_dec_apparent", ra_hours=ra_hours, dec_degs=dec_degs)

    def mount_goto_ra_dec_j2000(self, ra_hours, dec_degs):
        return self.request_with_status("/mount/goto_ra_dec_j2000", ra_hours=ra_hours, dec_degs=dec_degs)

    def mount_goto_alt_az(self, alt_degs, az_degs):
        return self.request_with_status("/mount/goto_alt_az", alt_degs=alt_degs, az_degs=az_degs)

    def mount_offset(self, **kwargs):
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

        return self.request_with_status("/mount/offset", **kwargs)

    def mount_park(self):
        return self.request_with_status("/mount/park")

    def mount_set_park_here(self):
        return self.request_with_status("/mount/set_park_here")

    def mount_tracking_on(self):
        return self.request_with_status("/mount/tracking_on")

    def mount_tracking_off(self):
        return self.request_with_status("/mount/tracking_off")

    def mount_follow_tle(self, tle_line_1, tle_line_2, tle_line_3):
        return self.request_with_status("/mount/follow_tle", line1=tle_line_1, line2=tle_line_2, line3=tle_line_3)

    def mount_model_add_point(self, ra_j2000_hours, dec_j2000_degs):
        return self.request_with_status("/mount/model/add_point", ra_j2000_hours=ra_j2000_hours, dec_j2000_degs=dec_j2000_degs)

    def mount_model_clear_points(self):
        return self.request_with_status("/mount/model/clear_points")

    def mount_model_save_as_default(self):
        return self.request_with_status("/mount/model/save_as_default")

    def mount_model_save(self, filename):
        return self.request_with_status("/mount/model/save", filename=filename)

    def mount_model_load(self, filename):
        return self.request_with_status("/mount/model/load", filename=filename)

    def focuser_enable(self):
        return self.request_with_status("/focuser/enable")

    def focuser_disable(self):
        return self.request_with_status("/focuser/disable")

    def focuser_goto(self, target):
        return self.request_with_status("/focuser/goto", target=target)

    def focuser_stop(self):
        return self.request_with_status("/focuser/stop")

    def rotator_enable(self):
        return self.request_with_status("/rotator/enable")

    def rotator_disable(self):
        return self.request_with_status("/rotator/disable")

    def rotator_goto_mech(self, target_degs):
        return self.request_with_status("/rotator/goto_mech", degs=target_degs)

    def rotator_goto_field(self, target_degs):
        return self.request_with_status("/rotator/goto_field", degs=target_degs)

    def rotator_offset(self, offset_degs):
        return self.request_with_status("/rotator/offset", degs=offset_degs)

    def rotator_stop(self):
        return self.request_with_status("/rotator/stop")

    def m3_goto(self, target_port):
        return self.request_with_status("/m3/goto", port=target_port)

    def m3_stop(self):
        return self.request_with_status("/m3/stop")

    def virtualcamera_take_image(self):
        """
        Returns a string containing a FITS image simulating a starfield
        at the current telescope position
        """
        return self.request("/virtualcamera/take_image")

    def virtualcamera_take_image_and_save(self, filename):
        """
        Request a fake FITS image from PWI4.
        Save the contents to the specified filename
        """

        contents = self.virtualcamera_take_image()
        f = open(filename, "wb")
        f.write(contents)
        f.close()

    ### Methods for testing error handling ######################

    def test_command_not_found(self):
        """
        Try making a request to a URL that does not exist.
        Useful for intentionally testing how the library will respond.
        """
        return self.request_with_status("/command/notfound")

    def test_internal_server_error(self):
        """
        Try making a request to a URL that will return a 500
        server error due to an intentionally unhandled error.
        Useful for testing how the library will respond.
        """
        return self.request_with_status("/internal/crash")

    def test_invalid_parameters(self):
        """
        Try making a request with intentionally missing parameters.
        Useful for testing how the library will respond.
        """
        return self.request_with_status("/mount/goto_ra_dec_apparent")

    ### Low-level methods for issuing requests ##################

    def request(self, command, **kwargs):
        return self.comm.request(command, **kwargs)

    def request_with_status(self, command, **kwargs):
        response_text = self.request(command, **kwargs)
        return self.parse_status(response_text)

    ### Status parsing utilities ################################

    def status_text_to_dict(self, response):
        """
        Given text with keyword=value pairs separated by newlines,
        return a dictionary with the equivalent contents.
        """

        # In Python 3, response is of type "bytes".
        # Convert it to a string for processing below
        if type(response) == bytes:
            response = response.decode('utf-8')

        response_dict = {}

        lines = response.split("\n")

        for line in lines:
            fields = line.split("=", 1)
            if len(fields) == 2:
                name = fields[0]
                value = fields[1]
                response_dict[name] = value

        return response_dict

    def parse_status(self, response_text):
        response_dict = self.status_text_to_dict(response_text)
        return PWI4Status(response_dict)



class Section(object):
    """
    Simple object for collecting properties in PWI4Status
    """

    pass

class PWI4Status:
    """
    Wraps the status response for many PWI4 commands in a class with named members
    """

    def __init__(self, status_dict):
        self.raw = status_dict  # Allow direct access to raw entries as needed

        self.site = Section()
        self.site.latitude_degs = self.get_float("site.latitude_degs")
        self.site.longitude_degs = self.get_float("site.longitude_degs")
        self.site.height_meters = self.get_float("site.height_meters")
        self.site.lmst_hours = self.get_float("site.lmst_hours")

        self.mount = Section()
        self.mount.is_connected = self.get_bool("mount.is_connected")
        self.mount.geometry = self.get_int("mount.geometry")
        self.mount.ra_apparent_hours = self.get_float("mount.ra_apparent_hours")
        self.mount.dec_apparent_degs = self.get_float("mount.dec_apparent_degs")
        self.mount.ra_j2000_hours = self.get_float("mount.ra_j2000_hours")
        self.mount.dec_j2000_degs = self.get_float("mount.dec_j2000_degs")
        self.mount.azimuth_degs = self.get_float("mount.azimuth_degs")
        self.mount.altitude_degs = self.get_float("mount.altitude_degs")
        self.mount.is_slewing = self.get_bool("mount.is_slewing")
        self.mount.is_tracking = self.get_bool("mount.is_tracking")
        self.mount.field_angle_here_degs = self.get_float("mount.field_angle_here_degs")
        self.mount.field_angle_at_target_degs = self.get_float("mount.field_angle_at_target_degs")
        self.mount.field_angle_rate_at_target_degs_per_sec = self.get_float("mount.field_angle_rate_at_target_degs_per_sec")

        self.mount.axis0 = Section()
        self.mount.axis0.is_enabled = self.get_bool("mount.axis0.is_enabled")
        self.mount.axis0.rms_error_arcsec = self.get_bool("mount.axis0.rms_error_arcsec")
        self.mount.axis0.dist_to_target_arcsec = self.get_float("mount.axis0.dist_to_target_arcsec")
        self.mount.axis0.servo_error_arcsec = self.get_float("mount.axis0.servo_error_arcsec")
        self.mount.axis0.position_degs = self.get_float("mount.axis0.position_degs")

        self.mount.axis1 = Section()
        self.mount.axis1.is_enabled = self.get_bool("mount.axis1.is_enabled")
        self.mount.axis1.rms_error_arcsec = self.get_bool("mount.axis1.rms_error_arcsec")
        self.mount.axis1.dist_to_target_arcsec = self.get_float("mount.axis1.dist_to_target_arcsec")
        self.mount.axis1.servo_error_arcsec = self.get_float("mount.axis1.servo_error_arcsec")
        self.mount.axis1.position_degs = self.get_float("mount.axis1.position_degs")

        self.mount.model = Section()
        self.mount.model.filename = self.get_string("mount.model.filename")
        self.mount.model.num_points_total = self.get_int("mount.model.num_points_total")
        self.mount.model.num_points_enabled = self.get_int("mount.model.num_points_enabled")
        self.mount.model.rms_error_arcsec = self.get_float("mount.model.rms_error_arcsec")

        self.focuser = Section()
        self.focuser.is_connected = self.get_bool("focuser.is_enabled")
        self.focuser.is_enabled = self.get_bool("focuser.is_enabled")
        self.focuser.position = self.get_float("focuser.position")
        self.focuser.is_moving = self.get_bool("focuser.is_moving")

        self.rotator = Section()
        self.rotator.is_connected = self.get_bool("rotator.is_connected")
        self.rotator.is_enabled = self.get_bool("rotator.is_enabled")
        self.rotator.mech_position_degs = self.get_float("rotator.mech_position_degs")
        self.rotator.field_angle_degs = self.get_float("rotator.field_angle_degs")
        self.rotator.is_moving = self.get_bool("rotator.is_moving")
        self.rotator.is_slewing = self.get_bool("rotator.is_slewing")

        self.m3 = Section()
        self.m3.port = self.get_int("m3.port")

    def get_bool(self, name):
        return self.raw[name].lower() == "true"

    def get_float(self, name):
        return float(self.raw[name])

    def get_int(self, name):
        return int(self.raw[name])

    def get_string(self, name):
        return self.raw[name]

    def __repr__(self):
        """
        Format all of the keywords and values we have received
        """

        max_key_length = max(len(x) for x in self.raw.keys())

        lines = []

        line_format = "%-" + str(max_key_length) + "s: %s"

        for key in sorted(self.raw.keys()):
            value = self.raw[key]
            lines.append(line_format % (key, value))
        return "\n".join(lines)

class PWI4HttpCommunicator:
    """
    Manages communication with PWI4 via HTTP.
    """

    def __init__(self, host="localhost", port=8220):
        self.host = host
        self.port = port

        self.timeout_seconds = 3

    def make_url(self, path, **kwargs):
        """
        Utility function that takes a set of keyword=value arguments
        and converts them into a properly formatted URL to send to PWI.
        Special characters (spaces, colons, plus symbols, etc.) are encoded as needed.

        Example:
          make_url("/mount/gotoradec2000", ra=10.123, dec="15 30 45") -> "http://localhost:8220/mount/gotoradec2000?ra=10.123&dec=15%2030%2045"
        """

        # Construct the basic URL, excluding the keyword parameters; for example: "http://localhost:8220/specified/path?"
        url = "http://" + self.host + ":" + str(self.port) + path + "?"

        # For every keyword=value argument given to this function,
        # construct a string of the form "key1=val1&key2=val2".
        keyword_values = list(kwargs.items()) # Need to explicitly convert this to list() for Python 3.x
        urlparams = urlencode(keyword_values)

        # In URLs, spaces can be encoded as "+" characters or as "%20".
        # This will convert plus symbols to percent encoding for improved compatibility.
        urlparams = urlparams.replace("+", "%20")

        # Build the final URL and return it.
        url = url + urlparams
        return url

    def request(self, path, **kwargs):
        """
        Issue a request to PWI using the keyword=value parameters
        supplied to the function, and return the response received from
        PWI.

        Example:
          pwi_request("/mount/gotoradec2000", ra=10.123, dec="15 30 45")

        will construct the appropriate URL and issue the request to the server.

        The server response payload will be returned, or an exception will be thrown
        if there was an error with the request.
        """

        # Construct the URL that we will request
        url = self.    (path, **kwargs)

        # Open a connection to the server, issue the request, and try to receive the response.
        # The server will return an HTTP Status Code as part of the response.
        # If the status code indicates an error, an HTTPError will be thrown.
        try:
            response = urlopen(url, timeout=self.timeout_seconds)
        except HTTPError as e:
            if e.code == 404:
                error_message = "Command not found"
            elif e.code == 400:
                error_message = "Bad request"
            elif e.code == 500:
                error_message = "Internal server error (possibly a bug in PWI)"
            else:
                error_message = str(e)

            try:
                error_details = e.read()  # Try to read the payload of the response for error information
                error_message = error_message + ": " + error_details
            except:
                pass # If that failed, we won't include any further details

            raise Exception(error_message) # TODO: Consider a custom exception here


        except Exception as e:
            # This will often be a urllib2.URLError to indicate that a connection
            # could not be made to the server, but we'll handle any exception here
            raise

        payload = response.read()
        return payload
