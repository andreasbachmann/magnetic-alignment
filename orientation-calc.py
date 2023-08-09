import math

def angle_from_north(tail, neck):    
  delta_easting = neck[0] - tail[0]
  delta_northing = neck[1] - tail[1]
  angle_rad = math.atan2(delta_northing, delta_easting)
  angle_deg = math.degrees(angle_rad)
  angle_from_east = (angle_deg + 360) % 360
  return (90 - angle_from_east) % 360
