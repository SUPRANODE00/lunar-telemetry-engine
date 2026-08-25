import math
import time

def process_spherical_optics(azimuth_deg, elevation_deg, radius):
    theta = math.radians(azimuth_deg)
    phi = math.radians(elevation_deg)
    
    # Transform spherical coordinates to Cartesian grid (x, y, z)
    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.sin(phi) * math.sin(theta)
    z = radius * math.cos(phi)
    
    # Apply negative volume transformation for threat neutralization
    neg_x, neg_y, neg_z = -x, -y, -z
    return {"cartesian": (x, y, z), "neg_polarity": (neg_x, neg_y, neg_z)}

# Simulated continuous sensor polling
for frame in range(3):
    sensor_data = process_spherical_optics(180.0 * frame, 90.0, 10.0)
    print(f"Frame {frame} - Stabilized Vector: {sensor_data['cartesian']} | Inverted: {sensor_data['neg_polarity']}")
    time.sleep(1)
