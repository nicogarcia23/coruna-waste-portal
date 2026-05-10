import pytest
from src.utils.geo import haversine, sort_by_distance, validate_coordinates


def test_haversine_distance_calculation():
    """Test Haversine distance calculation."""
    # Distance from (43.37, -8.39) to (43.38, -8.40) should be roughly 1.5km
    dist = haversine(43.37, -8.39, 43.38, -8.40)
    
    # Rough check: should be between 1000m and 2000m
    assert 1000 < dist < 2000


def test_validate_coordinates_valid():
    """Test coordinate validation with valid coordinates."""
    assert validate_coordinates(43.37, -8.39) is True
    assert validate_coordinates(0, 0) is True
    assert validate_coordinates(90, 180) is True
    assert validate_coordinates(-90, -180) is True


def test_validate_coordinates_invalid():
    """Test coordinate validation with invalid coordinates."""
    assert validate_coordinates(91, 0) is False  # Latitude > 90
    assert validate_coordinates(-91, 0) is False  # Latitude < -90
    assert validate_coordinates(0, 181) is False  # Longitude > 180
    assert validate_coordinates(0, -181) is False  # Longitude < -180


def test_sort_by_distance():
    """Test sorting containers by distance."""
    containers = [
        {
            "id": "c1",
            "location": {"type": "Point", "coordinates": [-8.40, 43.38]}
        },
        {
            "id": "c2",
            "location": {"type": "Point", "coordinates": [-8.39, 43.37]}
        },
        {
            "id": "c3",
            "location": {"type": "Point", "coordinates": [-8.38, 43.36]}
        }
    ]
    
    reference_lat, reference_lon = 43.37, -8.39
    sorted_containers = sort_by_distance(containers, reference_lat, reference_lon)
    
    # c2 is at the reference point, should be closest
    assert sorted_containers[0]["id"] == "c2"
    assert sorted_containers[0]["distance"] < 100  # Very close
