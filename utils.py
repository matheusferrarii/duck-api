from math import radians, cos, sin, asin, sqrt

def feet_to_cm(ft):
    return ft * 30.48

def lbs_to_g(lbs):
    return lbs * 453.59237

def yards_to_m(y):
    return y * 0.9144

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    R = 6371000
    return R * c
