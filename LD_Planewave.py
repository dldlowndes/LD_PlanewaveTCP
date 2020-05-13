import requests

# TODO:
#   - Separate classes for "model", "focuser", "rotator" etc?
#   - Handle errors gracefully
#   - validate input arg values?

class PWI_Device:
    def __init__(self, ip_Addr, port):
        self.req_Url = ":".join([ip_Addr, port])

    def _SendMsg(self, command, **kwargs):
        cmd_Url = "/".join([self.req_Url, *command])

        #todo: deal with failed
        response = requests.get(cmd_Url, kwargs)
        #todo: parse response
        return response

class Planewave_Mount(PWI_Device):
    def __init__(self, ip_Addr="127.0.0.1", port="8220"):
        super().__init__(ip_Addr, port)

    def Connect(self):
        return self._SendMsg(["mount", "connect"])

    def Disconnect(self):
        return self._SendMsg(["mount", "disconnect"])

    def Enable(self):
        responses = []
        for axis_Number in [0, 1]:
            responses.append(
                    self._SendMsg(["mount", "enable"], axis=axis_Number)
                    )
        return *responses

    def Disable(self):
        responses = []
        for axis_Number in [0, 1]:
            responses.append(
                    self._SendMsg(["mount", "disable"], axis=axis_Number)
                    )
        return *responses

    def Home(self):
        return self._SendMsg(["mount", "find_home"])

    def Stop(self):
        return self._SendMsg(["mount", "stop"])

    def Goto_RaDec_Apparent(self, ra_Hours, dec_Degrees):
        return self._SendMsg(["mount", "goto_ra_dec_apparent"],
                  ra_hours=ra_Hours,
                  dec_degs=dec_Degrees)

    def Goto_RaDec_J2000(self):
        return self._SendMsg(["mount", "goto_ra_dec_j2000"],
                  ra_hours=ra_Hours,
                  dec_degs=dec_Degrees)

    def Goto_AltAz(self, alt_Degrees, az_Degrees):
        return self._SendMsg(["mount", "goto_alt_az"],
                  alt_degs=alt_Degrees,
                  az_degs=az_Degrees)

    def Mount_Offset(self):
        raise NotImplementedError

    def Park(self):
        return self._SendMsg(["mount", "park"])

    def Park_Here(self):
        return self._SendMsg(["mount", "set_park_here"])

    def Tracking_On(self):
        return self._SendMsg(["mount", "tracking_on"])

    def Tracking_Off(self):
        return self._SendMsg(["mount", "tracking_off"])

    def Follow_TLE(self, tle_Lines):
        assert len(tle_Lines) == 3 # todo: more validation of tles
        return self._SendMsg(["mount", "follow_tle"],
                  line1=tle_Lines[0],
                  line2=tle_Lines[1],
                  line3=tle_Lines[2])

if __name__ == "__main__":
    myMount = Planewave_Mount("http://192.168.1.170", "8220")
    response = myMount.Goto_RaDec_Apparent(0,0)
    for line in response.iter_lines():
        print(line)