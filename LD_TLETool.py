import requests

# TODO: Make TLE class (instead of having separate methods for the way the TLE is returned, can return a TLE object and it has methods to return in different representations
# TODO: Search for satellites which will be visible (soon, here)

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
    print(iss_tle)
