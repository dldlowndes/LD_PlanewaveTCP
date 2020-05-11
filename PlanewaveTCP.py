#!/usr/bin/python3
"""
A way to control a Planewave telescope by sending messages over TCP to
a port opened by the PWI software running on Windows.
"""

__author__ = "David Lowndes"
__email__ = "david.lowndes@bristol.ac.uk"
__status__ = "Prototype"

import select
import socket
import time

class PlanewaveTCP:
    def __init__(self, ip_Addr="127.0.0.1", tcp_Port=8220):
        """
        Set up the TCP connection.
        """
        self.my_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_Socket.connect((ip_Addr, tcp_Port))

        ## I think this is useful in reducing latency
        ## TODO: Test if this is useful!
        self.my_Socket.setblocking(False)
        self.timeout = 5 #seconds

    def __SendMsg(self, command, args=None):
        """
        Send a message to the PWI software to do something.
        Tries to handle args given as strings or numbers
        """
        message = command + "\n"

        ## Handle as many different formats of args as possible.
        ## TODO: Numpy array?
        if args is not None:
            if type(args) == str:
                pass
            elif type(args) in [list, tuple]:
                args = "\n".join(map(str, args))
            else:
                ## It's either a single int/float or something that will crash this
                args = str(args)

            ## Construct entire command message.
            message += args + "\n"
        else:
            ## There are no arguments.
            pass
        my_Message = message.encode("ascii")
        print(my_Message)
        self.my_Socket.sendall(my_Message)

    def __RecvMsg(self):
        """
        Receive a one line long response from the PWI software.
        """
        ## TODO: figure out timeout in here.
        response = ""
        timer = 0
        while not self.SocketIsReadable():
            ## If there's nothing at the socket now. Wait until
            ##there is
            sleep(0.1)
            timer += 0.1
            print("check")
            if timer > self.timeout:
                break
        while not response.endswith("\n"):
            response += self.my_Socket.recv(1).decode("UTF-8")
        return response

    def SocketIsReadable(self):
        """
        Check if there is anything waiting on the socket.
        """
        return len(select.select([self.my_Socket], [], [self.my_Socket], 2)[0]) > 0

    def Close(self):
        """
        Close the TCP socket (I assume on the host?)
        No response expected.
        """
        self.__SendMsg("close")

    def GetStatus(self):
        """
        Ask for the status. The response is many lines so the
        receving is done specially for this method.
        """
        self.__SendMsg("status")
        ##TODO: Parse the response into some struct so it can be queried later.

        ## "Status" is the only command that returns a multi
        ## line response so handle it separately.
        response = ""
        while(self.SocketIsReadable()):
            data = self.my_Socket.recv(1)
            if not data:
                break
            else:
                response += data.decode("UTF-8")
        return response

    def Goto(self, ra_Apparent, dec_Apparent):
        """
        Begin slewing to specified RA/Dec
        coordinates, in the "apparent" coordinate
        frame. Slewing will begin immediately after
        receiving the final argument
        Expected response: OK|ERROR
        """
        assert (type(ra_Apparent) == float)
        assert (type(dec_Apparent) == float)
        self.__SendMsg("gotoradecapp", [ra_Apparent, dec_Apparent])
        return self.__RecvMsg()

    def TLE(self, sat_Name, line_1, line_2):
        """
        Begin tracking a satellite described by the
        specified TLE. The first line is the satellite
        name. The second and third lines contain the
        orbital elements
        Expected response: OK|ERROR
        """
        tle_Set = [sat_Name, line_1, line_2]
        assert all([type(x) == str for x in tle_Set])
        self.__SendMsg("tle", tle_Set)
        return self.__RecvMsg()

    def Track(self):
        """
        Begin sidereal tracking at the current mount
        location
        Expected response: OK
        """
        self.__SendMsg("track")
        return self.__RecvMsg()

    def Stop(self):
        """
        Stop all motion on the mount.
        Expected response: OK
        """
        self.__SendMsg("stop")
        return self.__RecvMsg()

    def SetTimeOffset(self, offset_Seconds):
        """
        Apply a time offset to the target coordinate
        calculations. Useful for satellite tracking
        Expected response: OK|ERROR
        """
        ## TODO: Save offset as a member variable so it can be queried later.
        self.__SendMsg("settimeoffset", offset_Seconds)
        return self.__RecvMsg()

    def SetRaDecOffset(self, ra_Offset, dec_Offset):
        """
        Apply the specified RA and Dec offset to the
        current tracking target.
        Expected response: OK|ERROR
        """
        ## TODO: Save offset as a member variable so it can be queried later.
        self.__SendMsg("radecoffset", [ra_Offset, dec_Offset])
        return self.__RecvMsg()

    def PulseGuide(self, direction, duration_ms):
        """
        Mimic the behavior of the ASCOM
        PulseGuide() method
        Expected response: OK|ERROR
        """
        self.__SendMsg("pulseguide", [direction, duration_ms])
        return self.__RecvMsg()


if __name__ == "__main__":
    my_PW = PlanewaveTCP("127.0.0.1", 8220)

    print(my_PW.GetStatus())

    print(my_PW.Goto(5.0, 5.0))
    time.sleep(1)

    print(my_PW.Stop())
    time.sleep(1)

    print(my_PW.Track())
    time.sleep(1)

    print(my_PW.Stop())
    time.sleep(1)

    print(my_PW.Close())
    time.sleep(1)

