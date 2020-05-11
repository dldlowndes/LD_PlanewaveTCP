# Sample code to follow a TLE entry retrieved fromfrom
# https://www.celestrak.com/NORAD/elements/geo.txt
# Also perform some position offsets around that target.
#
# To see a demonstration of this code in action,
# please visit https://www.youtube.com/watch?v=6f52QBC5k9k

import time

from pwi4_client import PWI4

# Boilerplate: define a function to wait for user input that
# works with both Python2 and Python3
try:
    wait_for_input = raw_input  # For Python 2
except NameError:
    wait_for_input = input  # For Python 3



# Create the PWI4 object
print("Connecting to PWI4...")
pwi4 = PWI4()


# Make sure mount is connected and motors are energized
print("Connecting to mount and enabling motors...")
pwi4.mount_connect()
pwi4.mount_enable(0)
pwi4.mount_enable(1)

# ARSAT 2 is a geosynchronous satellite that should typically be visible
# from North and South America. The TLE data was retrieved on 2020-05-09.
# The position will become increasingly inaccurate the farther you are
# from this data. Updated TLE data for ARSAT 2 should be retrieved from:
# https://www.celestrak.com/NORAD/elements/geo.txt
tle1 = "ARSAT 2"
tle2 = "1 40941U 15054B   20130.57823185 -.00000235  00000-0  00000-0 0  9999"
tle3 = "2 40941   0.0571 108.1874 0001980 312.1056 294.7159  1.00271294 16963"

# If you are instead testing from Europe or Africa, EUTELSAT 33E
# should be a good target that is always above the horizon:
#tle1 = "EUTELSAT 33E"
#tle2 = "1 33750U 09008B   20130.51155170  .00000145  00000-0  00000-0 0  9996"
#tle3 = "2 33750   0.0630  32.6825 0004272  13.0575  39.2896  1.00274144 41095"

# If testing from Asia or Australia, EXPRESS-AM3 may be a good target:
#tle1 = "EXPRESS-AM3"
#tle2 = "1 28707U 05023A   20130.62624640 -.00000333  00000-0  00000-0 0  9990"
#tle3 = "2 28707   1.7484  90.9080 0001407 311.8879 153.5809  1.00270011 54489"


print("Selected TLE:")
print(tle1)
print(tle2)
print(tle3)
wait_for_input("Press enter to begin slewing to follow this TLE")
pwi4.mount_follow_tle(tle1, tle2, tle3)
time.sleep(1) # Give the mount a chance to begin slewing

# Monitor distance to target to determine when we have arrived
while True:
    status = pwi4.status()
    dist0 = status.mount.axis0.dist_to_target_arcsec
    dist1 = status.mount.axis1.dist_to_target_arcsec
    print("Distance to target: %.1f x %.1f arcsec" % (dist0, dist1))

    # If both axes are within 2 arcseconds of target,
    # break out of loop
    if abs(dist0) < 2 and abs(dist1) < 2:
        print("Arrived at target")
        break

    time.sleep(0.2)

# Perform a 20 arcsecond offset in the native "axis0" coordinates of the mount,
# For an EQ mount: Axis0 = RA axis, Axis1 = Dec axis
# For an Alt-Az mount: Axis0 = Azimuth axis, Axis1 = Altitude axis
#
# As long as you do not rotate your camera, these directions should remain consistent
# in your field of view, so this coordiante system is a good candidate for performing 
# centering/guiding corrections.
wait_for_input("Press Enter to offset mount 20 arcsec in Axis0")
pwi4.mount_offset(axis0_add_arcsec=20)


# Make a 20 arcsecond correction in the axis1 direction
wait_for_input("Press Enter to offset mount 20 arcsec in Axis1")
pwi4.mount_offset(axis1_add_arcsec=20)

# You can also set both offsets simultaneously
wait_for_input("Press Enter to offset 20 arcsec in both Axis0 and Axis1")
pwi4.mount_offset(axis0_add_arcsec=20, axis1_add_arcsec=20)

# You can also set both offsets simultaneously
wait_for_input("Press Enter to clear all accumulated offsets and return to original position")
pwi4.mount_offset(axis0_reset=0, axis1_reset=0)

# Other coordinate systems are available as well, such as RA/Dec
wait_for_input("Press Enter to offset 20 arcsec in Dec")
pwi4.mount_offset(dec_add_arcsec=20)

wait_for_input("Press Enter to offset 20 arcsec in RA")
pwi4.mount_offset(ra_add_arcsec=20)

# You can also set offset tracking rates in any of these axes
wait_for_input("Press Enter to move 5 arcsec/sec along Axis1")
pwi4.mount_offset(axis1_set_rate_arcsec_per_sec=5)

wait_for_input("Press Enter to stop moving along Axis1")
pwi4.mount_offset(axis1_stop_rate=0)


# Stop
wait_for_input("Press Enter to stop mount")
pwi4.mount_stop()
