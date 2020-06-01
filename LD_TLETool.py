import requests

# TODO: Make TLE class (instead of having separate methods for the way the TLE is returned, can return a TLE object and it has methods to return in different representations
# TODO: Search for satellites which will be visible (soon, here) - use https://in-the-sky.org/satpasses.php

class My_TLE:
    """
    Container to make accessing elements of a TLE easier.
    """
    def __init__(self, tle):
        if isinstance(tle, str):
            tle = tle.split("\n")
        # falls through to this one too!
        if isinstance(tle, (list, tuple)):
            assert len(tle) == 3
            self.tle_Dict = {
                "line0": tle[0],
                "line1": tle[1],
                "line2": tle[2]
                }
        elif isinstance(tle, dict):
            self.tle_Dict = tle
        
        
        line1_Split = self.tle_Dict["line1"].split()
        line2_Split = self.tle_Dict["line2"].split()
        self.name = self.tle_Dict["line0"]
        self.line1 = line1_Split[0]
        self.catalog_Number = line1_Split[1][:-1]
        self.classification = line1_Split[1][-1:]
        self.designator = line1_Split[2]
        self.epoch = line1_Split[3]
        self.first_Derivative = line1_Split[4]
        self.second_Derivative = line1_Split[5]
        self.drag_Term = line1_Split[6]
        self.ephemeris_Type = line1_Split[7]
        self.set_Number = line1_Split[8][:-1]
        self.checksum_1 = line1_Split[8][-1:]
        
        self.line2 = line2_Split[0]
        #assert line2_Split[1] == self.catalog_Number
        self.inclination = line2_Split[2]
        self.raan = line2_Split[3]
        self.eccentricity = line2_Split[4]
        self.perigree = line2_Split[5]
        self.mean_anomaly = line2_Split[6]
        self.mean_motion = line2_Split[7][:10]
        self.revolution_Number = line2_Split[7][11:-1]
        self.checksum_2 = line2_Split[7][-1:]
        
    @property
    def Dict(self):
        return self.tle_Dict
    
    @property
    def List(self):
        return list(self.tle_Dict.values())
    
    @property
    def String(self):
        return "\n".join(list(self.tle_Dict.values()))
    
    def __getitem__(self, i):
        return list(self.tle_Dict.values())[i]

class TLE_List:
    """
    Get TLE database from a file (local or internet).
    """
    def __init__(self, path, fetch_from_internet):
        """
        Get the TLE data and sort it into a nice structure.
        """
        if fetch_from_internet:
            # Get list from the internet.
            req = requests.get(path)
            flatlist = req.text.split("\r\n")
        else:
            # Load the list locally.
            data = open(path).read()
            flatlist = data.split("\n")

        # Every 3rd line is a satellite name. Extract them and trim the whitespace off.
        tle_Names = map(lambda x: x.rstrip(), flatlist[0::3])
        # Reshape the data from the file grouped into threes
        tle_List = zip(flatlist[0::3], flatlist[1::3], flatlist[2::3])
        # Put the data into a dict
        self.tle_Dict = {key:data for (key, data) in zip(tle_Names, tle_List)}

        # Hilarious one liner to do the above:
        # {x.rstrip():(x,y,z) for x,y,z in itertools.zip_longest(*[iter(flatlist)] * 3)}

    def Search_Keys(self, search_String):
        """
        Return all dict keys that contain a substring (case insensitive)
        """

        search_Keys = list(filter(lambda x: search_String.lower() in x.lower(), self.tle_Dict.keys()))
        if len(search_Keys) == 1:
            search_Keys = search_Keys[0]
        return search_Keys

    def Get_TLE_String(self, key):
        return "\n".join(self.Get_TLE_Elements(key))

    def Get_TLE_Elements(self, key):
        return self.tle_Dict[key]




if __name__ == "__main__":
    my_tles = TLE_List("active.txt", False)

    iss_Key = my_tles.Search_Keys("zarya")
    iss_tle = my_tles.Get_TLE_String(iss_Key)
    tle = my_tles.tle_Dict["ISS (ZARYA)"]
    print(iss_tle)
    
    my = My_TLE(tle)
