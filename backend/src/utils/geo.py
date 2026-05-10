import math
from typing import List, Tuple


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on earth (in meters).
    
    Args:
        lat1, lon1: First point (latitude, longitude) in degrees
        lat2, lon2: Second point (latitude, longitude) in degrees
    
    Returns:
        Distance in meters
    """
    R = 6371000  # Earth radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def sort_by_distance(
    containers: List[dict], ref_lat: float, ref_lon: float
) -> List[dict]:
    """Sort containers by distance from reference point."""
    containers_with_dist = []
    for container in containers:
        loc = container.get("location", {})
        if loc.get("type") == "Point" and loc.get("coordinates"):
            coords = loc["coordinates"]
            # GeoJSON is [lon, lat]
            dist = haversine(ref_lat, ref_lon, coords[1], coords[0])
            container["distance"] = dist
            containers_with_dist.append(container)
    
    return sorted(containers_with_dist, key=lambda x: x.get("distance", float("inf")))


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude ranges."""
    return -90 <= lat <= 90 and -180 <= lon <= 180
