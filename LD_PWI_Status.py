class PWI_Status:
    """
    Big class to hold all the statuses reported by PWI4
    """
    def __init__(self):
        """
        Make empty instances for all statuses.
        """
        
        self._version = ""
        self.site = Site_Status()
        self.mount = Mount_Status()
        self.focuser = Focuser_Status()
        self.rotator = Rotator_Status()
        self.m3 = M3_Status()
        self.autofocus = AutoFocus_Status()

    @property        
    def version(self):
        return self._version
    
    @version.setter
    def version(self, value):
        self._version = value
    
    def Update(self, response):
        """
        Take the response from the requests package, parse and set member
        variables in this class.
        """
        string_status = {}
        for line in response.iter_lines():
            line = line.decode()
            dotted_keys, value = line.split("=")
            string_status[dotted_keys] = value
            print(line)
        
        self.version = string_status["pwi4.version"]
        
        self.site.latitude = string_status["site.latitude_degs"]
        self.site.longitude = string_status["site.longitude_degs"]
        self.site.height = string_status["site.height_meters"]
        
        self.mount.is_connected = string_status["mount.is_connected"]
        self.mount.geometry = string_status["mount.geometry"]
        self.mount.ra_apparent = string_status["mount.ra_apparent_hours"]
        self.mount.dec_apparent = string_status["mount.dec_apparent_degs"]
        self.mount.ra_j2000 = string_status["mount.ra_j2000_hours"]
        self.mount.dec_j2000 = string_status["mount.dec_j2000_degs"]
        self.mount.target_ra_apparent = string_status["mount.target_ra_apparent_hours"]
        self.mount.target_dec_apparent = string_status["mount.target_dec_apparent_degs"]
        self.mount.altitude = string_status["mount.altitude_degs"]
        self.mount.azimuth = string_status["mount.azimuth_degs"]
        self.mount.is_slewing = string_status["mount.is_slewing"]
        self.mount.is_tracking = string_status["mount.is_tracking"]
        self.mount.field_angle_here = string_status["mount.field_angle_here_degs"]
        self.mount.field_angle_target = string_status["mount.field_angle_at_target_degs"]
        self.mount.field_angle_rate_target = string_status["mount.field_angle_rate_at_target_degs_per_sec"]
        self.mount.path_angle_target = string_status["mount.path_angle_at_target_degs"]
        self.mount.path_angle_target_rate = string_status["mount.path_angle_rate_at_target_degs_per_sec"]
        
        self.mount.axis0.is_enabled = string_status["mount.axis0.is_enabled"]
        self.mount.axis0.rms_error = string_status["mount.axis0.rms_error_arcsec"]
        self.mount.axis0.dist_to_target = string_status["mount.axis0.dist_to_target_arcsec"]
        self.mount.axis0.servo_error = string_status["mount.axis0.servo_error_arcsec"]
        self.mount.axis0.position = string_status["mount.axis0.position_degs"]

        self.mount.axis1.is_enabled = string_status["mount.axis1.is_enabled"]
        self.mount.axis1.rms_error = string_status["mount.axis1.rms_error_arcsec"]
        self.mount.axis1.dist_to_target = string_status["mount.axis1.dist_to_target_arcsec"]
        self.mount.axis1.servo_error = string_status["mount.axis1.servo_error_arcsec"]
        self.mount.axis1.position = string_status["mount.axis1.position_degs"]
        
        self.mount.model.filename = string_status["mount.model.filename"]
        self.mount.model.n_points_total = string_status["mount.model.num_points_total"]
        self.mount.model.n_points_enabled = string_status["mount.model.num_points_enabled"]
        self.mount.model.rms_error = string_status["mount.model.rms_error_arcsec"]
        
        self.focuser.is_connected = string_status["focuser.is_connected"]
        self.focuser.is_enabled = string_status["focuser.is_enabled"]
        self.focuser.position = string_status["focuser.position"]
        self.focuser.is_moving = string_status["focuser.is_moving"]

        self.rotator.is_connected = string_status["rotator.is_connected"]
        self.rotator.is_enabled = string_status["rotator.is_enabled"]
        self.rotator.mech_position = string_status["rotator.mech_position_degs"]
        self.rotator.field_angle = string_status["rotator.field_angle_degs"]
        self.rotator.is_moving = string_status["rotator.is_moving"]
        self.rotator.is_slewing = string_status["rotator.is_slewing"]
        
        self.m3.port = string_status["m3.port"]
        
        self.autofocus.is_connected = string_status["autofocus.is_running"]
        self.autofocus.success = string_status["autofocus.success"]
        self.autofocus.best_position = string_status["autofocus.best_position"]
        self.autofocus.tolerance = string_status["autofocus.tolerance"]

    def __str__(self):
        out_Values = [
            f"Version: {self.version}",
            f"----- Site status: -----",
            str(self.site),
            f"----- Mount status: -----",
            str(self.mount),
            f"----- Focuser status: -----",
            str(self.focuser),
            f"----- Rotator status: -----",
            str(self.rotator),
            f"----- M3 status: -----",
            str(self.m3),
            f"----- Autofocus status: -----",
            str(self.autofocus)
            ]
        return "\n".join(out_Values)

class Site_Status:
    """
    The status report relating to the site of the telescope
    [latitude, longitude, height, local siderial time]
    """
    
    def __init__(self):
        self._latitude = 0.0
        self._longitude = 0.0
        self._height = 0
        self._lst = 0.0
        
    def __str__(self):
        return "\n".join([
            f"\tSite latitude = {self._latitude} degrees",
            f"\tSite longitude = {self._longitude} degrees",
            f"\tSite height = {self._height} metres",
            f"\tSite local siderial time = {self._lst} hours"
            ])
        
    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        self._latitude = float(value)
         
    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        self._longitude = float(value)
        
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        
    @property
    def lst(self):
        return self._lst
    
    @lst.setter
    def lst(self, value):
        self._lst = value       
    
    
class Mount_Status:
    """
    The status report relating to the telescope mount itself
    """
    def __init__(self):
        self._is_connected = False
        self._geometry = "Alt-Az"
        self._ra_apparent = 0.0
        self._dec_apparent = 0.0
        self._ra_j2000 = 0.0
        self._dec_j2000 = 0.0
        self._target_ra_apparent = 0.0
        self._target_dec_apparent = 0.0
        self._altitude = 0.0
        self._azimuth = 0.0
        self._is_slewing = False
        self._is_tracking = False
        self._field_angle_here = 0.0
        self._field_angle_target = 0.0
        self._field_angle_rate_target = 0.0
        self._path_angle_target = 0.0
        self._path_angle_rate_target = 0.0
        
        self.axis0 = Axis_Status()
        self.axis1 = Axis_Status()
        self.model = Model_Status()
        
        self.geometry_modes = {
            "0": "Alt-Az",
            "1": "Equatorial Fork",
            "2": "German Equatorial"
            }
    
    def __str__(self):
        return "\n".join([
            f"\tIs connected: {self._is_connected}",
            f"\tGeometry: {self._geometry}",
            f"\tRA (apparent) = {self._ra_apparent} hours",
            f"\tDEC (apparent) = {self._dec_apparent} degrees",
            f"\tRA (J2000) = {self._ra_j2000} hours",
            f"\tDEC (J2000) = {self._dec_j2000} degrees",
            f"\tTarget RA (apparent) = {self._target_ra_apparent} hours",
            f"\tTarget DEC (apparent) = {self._target_dec_apparent} degrees",
            f"\tAltitude = {self._altitude} degrees",
            f"\tAzimuth = {self._azimuth} degrees",
            f"\tSlewing?: {self._is_slewing}",
            f"\tTracking?: {self._is_tracking}",
            f"\tField angle here = {self._field_angle_here} degrees",
            f"\tField angle at target = {self._field_angle_target} degrees",
            f"\tField angle rate at target = {self._field_angle_rate_target} degrees/sec",
            f"\tPath angle at target = {self._path_angle_target} degrees",
            f"\tPath angle rate at target = {self._path_angle_rate_target} degrees/sec",
            f"\tAxis0:",
            str(self.axis0),
            f"\tAxis1:",
            str(self.axis1),
            f"\tPointing model:",
            str(self.model)
            ])
        
    @property
    def is_connected(self):
        return self._is_connected
    
    @is_connected.setter
    def is_connected(self, value):
        self._is_connected = bool(value)
        
    @property
    def geometry(self):
        return self._geometry
    
    @geometry.setter
    def geometry(self, value):
        self._geometry = self.geometry_modes[value]
        
    @property
    def ra_apparent(self):
        return self._ra_apparent
    
    @ra_apparent.setter
    def ra_apparent(self, value):
        self._ra_apparent = float(value)
                
    @property
    def dec_apparent(self):
        return self._dec_apparent
    
    @dec_apparent.setter
    def dec_apparent(self, value):
        self._dec_apparent = float(value)
                
    @property
    def ra_j2000(self):
        return self._ra_j2000
    
    @ra_j2000.setter
    def ra_j2000(self, value):
        self._ra_j2000 = float(value)
                
    @property
    def dec_j2000(self):
        return self._dec_j2000
    
    @dec_j2000.setter
    def dec_j2000(self, value):
        self._dec_j2000 = float(value)
    
    @property
    def target_ra_apparent(self):
        return self._target_ra_apparent
    
    @target_ra_apparent.setter
    def target_ra_apparent(self, value):
        self._target_ra_apparent = float(value)
                
    @property
    def target_dec_apparent(self):
        return self._target_dec_apparent
    
    @target_dec_apparent.setter
    def target_dec_apparent(self, value):
        self._target_dec_apparent = float(value)
            
    @property
    def altitude(self):
        return self._altitude
    
    @altitude.setter
    def altitude(self, value):
        self._altitude = float(value)
                
    @property
    def azimuth(self):
        return self._azimuth
    
    @azimuth.setter
    def azimuth(self, value):
        self._azimuth = float(value)
                 
    @property
    def is_slewing(self):
        return self._is_slewing
    
    @is_slewing.setter
    def is_slewing(self, value):
        self._is_slewing = bool(value)
                 
    @property
    def is_tracking(self):
        return self._is_tracking
    
    @is_tracking.setter
    def is_tracking(self, value):
        self._is_tracking = bool(value)
                 
    @property
    def field_angle_here(self):
        return self._field_angle_here
    
    @field_angle_here.setter
    def field_angle_here(self, value):
        self._field_angle_here = float(value)
                 
    @property
    def field_angle_target(self):
        return self._field_angle_target
    
    @field_angle_target.setter
    def field_angle_target(self, value):
        self._field_angle_target = float(value)
                 
    @property
    def field_angle_rate_target(self):
        return self._field_angle_rate_target
    
    @field_angle_rate_target.setter
    def field_angle_rate_target(self, value):
        self._field_angle_rate_target = float(value)
                 
    @property
    def path_angle_target(self):
        return self._path_angle_target
    
    @path_angle_target.setter
    def path_angle_target(self, value):
        self.__path_angle_target = float(value)
                 
    @property
    def path_angle_rate_target(self):
        return self._path_angle_rate_target
    
    @path_angle_rate_target.setter
    def path_angle_rate_target(self, value):
        self._path_angle_rate_target = float(value)
                  
        
class Axis_Status:
    """
    Status of a specific axis of the telescope mount
    """
    def __init__(self):
        self._is_enabled = False
        self._rms_error = 0.0
        self._dist_to_target = 0.0
        self._servo_error = 0.0
        self._position = 0.0
    
    def __str__(self):
        return "\n".join([
            f"\t\tEnabled?: {self._is_enabled}",
            f"\t\tRMS Error =  {self._rms_error} arcsec",
            f"\t\tDistance to target = {self._dist_to_target} arcsec",
            f"\t\tServo error = {self._servo_error} arcsec",
            f"\t\tPosition = {self._position} degrees"
            ])
    
    @property
    def is_enabled(self):
        return self._is_enabled
    
    @is_enabled.setter
    def is_enabled(self, value):
        self._is_enabled = bool(value)
        
    @property
    def rms_error(self):
        return self._rms_error
    
    @rms_error.setter
    def rms_error(self, value):
        self._rms_error = float(value)
        
    @property
    def dist_to_target(self):
        return self._dist_to_target
    
    @dist_to_target.setter
    def dist_to_target(self, value):
        self._dist_to_target = float(value)
        
    @property
    def servo_error(self):
        return self._servo_error
    
    @servo_error.setter
    def servo_error(self, value):
        self._servo_error = float(value)

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = float(value)

class Model_Status:
    """
    Something to do with the pointing model of the mount
    (can't find any documentation about this)
    """
    def __init__(self):
        self._filename = ""
        self._n_points_total = 0
        self._n_points_enabled = 0
        self._rms_error = 0.0
        
    def __str__(self):
        return "\n".join([
            f"\t\tFilename: {self._filename}",
            f"\t\tnum points total = {self._n_points_total}",
            f"\t\tnum points enabled = {self._n_points_enabled}",
            f"\t\tRMS error {self._rms_error} arcsec"
            ])

    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, value):
        self._filename = value
    
    @property
    def n_points_total(self):
        return self._n_points_total
    
    @n_points_total.setter
    def n_points_total(self, value):
        self._n_points_total = int(value)
        
    @property
    def n_points_enabled(self):
        return self._n_points_enabled
    
    @n_points_enabled.setter
    def n_points_enabled(self, value):
        self._n_points_enabled = int(value)
        
    @property
    def rms_error(self):
        return self._rms_error
    
    @rms_error.setter
    def rms_error(self, value):
        self._rms_error = float(value)


class Focuser_Status:
    """
    The status report relating to the telescope focusser
    """
    
    def __init__(self):
        self._is_connected = False
        self._is_enabled = False
        self._position = 0.0
        self._is_moving = False

    def __str__(self):
        return "\n".join([
            f"\tConnected?: {self._is_connected}",
            f"\tEnabled?: {self._is_enabled}",
            f"\tPosition = {self._position}",
            f"\tMoving?: {self._is_moving}"
            ])

    @property
    def is_connected(self):
        return self._is_connected
    
    @is_connected.setter
    def is_connected(self, value):
        self._is_connected = bool(value)
    
    @property
    def is_enabled(self):
        return self._is_enabled
    
    @is_enabled.setter
    def is_enabled(self, value):
        self._is_enabled = bool(value)
        
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = float(value)
        
    @property
    def is_moving(self):
        return self._is_moving
    
    @is_moving.setter
    def is_moving(self, value):
        self._is_moving = bool(value)

class Rotator_Status:
    """
    The status report relating to the telescope rotator
    """    
    
    def __init__(self):
        self._is_connected = False
        self._is_enabled = False
        self._mech_position = 0.0
        self._field_angle = 0.0
        self._is_moving = False
        self._is_slewing = False

    def __str__(self):
        return "\n".join([
            f"\tConnected?: {self._is_connected}",
            f"\tEnabled?: {self._is_enabled}",
            f"\tMechanical position = {self._mech_position} degrees",
            f"\tField angle = {self._field_angle} degrees",
            f"\tMoving?: {self._is_moving}",
            f"\tSlewing?: {self._is_slewing}",
            ])

    @property
    def is_connected(self):
        return self._is_connected
    
    @is_connected.setter
    def is_connected(self, value):
        self._is_connected = bool(value)

    @property
    def is_enabled(self):
        return self._is_enabled
    
    @is_enabled.setter
    def is_enabled(self, value):
        self._is_enabled = bool(value)
        
    @property
    def mech_position(self):
        return self._mech_position
    
    @mech_position.setter
    def mech_position(self, value):
        self._mech_position = float(value)
        
    @property
    def field_angle(self):
        return self._field_angle
    
    @field_angle.setter
    def field_angle(self, value):
        self._field_angle = float(value)
        
    @property
    def is_moving(self):
        return self._is_moving
    
    @is_moving.setter
    def is_moving(self, value):
        self._is_moving = bool(value)

    @property
    def is_slewing(self):
        return self._is_slewing
    
    @is_slewing.setter
    def is_slewing(self, value):
        self._is_slewing = bool(value)
        
class M3_Status:
    """
    The status report relating to ... ?
    """
    
    def __init__(self):
        self._port = 0
    
    def __str__(self):
        return "\n".join([
            f"\tPort: {self._port}"
            ])
    
    @property
    def port(self):
        return self._port
    
    @port.setter
    def port(self, value):
        self._port = int(value)
        
class AutoFocus_Status:
    """
    The status report relating to the telescope autofocus
    """
    
    def __init__(self):
        self._is_running = False
        self._success = False
        self._best_position = 0.0
        self._tolerance = 0.0
    
    def __str__(self):
        return "\n".join([
            f"\tRunning?: {self._is_running}",
            f"\tSuccess?: {self._success}",
            f"\tBest position = {self._best_position}",
            f"\tTolerance = {self._tolerance}"
            ])
    
    @property
    def is_running(self):
        return self._is_running
    
    @is_running.setter
    def is_running(self, value):
        self._is_running = bool(value)

    @property
    def success(self):
        return self._success
    
    @success.setter
    def success(self, value):
        self._success = bool(value)        

    @property
    def best_position(self):
        return self._best_position
    
    @best_position.setter
    def best_position(self, value):
        self._best_position = float(value)
        
    @property
    def tolerance(self):
        return self._tolerance
    
    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = float(value)