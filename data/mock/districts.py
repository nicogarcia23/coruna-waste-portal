import json
import logging
from pathlib import Path
import geopandas as gpd
from shapely.geometry import shape
import requests

LOG = logging.getLogger(__name__)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def fetch_district_polygons(district_names, cache_path):
    cache = Path(cache_path)
    if cache.exists():
        return gpd.read_file(str(cache))

    # Build Overpass query for A Coruña administrative area and given district names
    name_filters = "|".join(district_names)
    query = f"""
    [out:json][timeout:25];
    area["name"="A Coruña"]["admin_level"="8"]->.city;
    (
      rel(area.city)["boundary"="administrative"]["name"~"{name_filters}"];
    );
    out geom;
    """
    try:
        r = requests.post(OVERPASS_URL, data={'data': query}, timeout=30)
        r.raise_for_status()
        data = r.json()
        features = []
        for el in data.get('elements', []):
            if 'tags' not in el:
                continue
            geom = None
            if el.get('type') == 'relation' and 'members' in el:
                # Overpass returns relation with members - skip complex parsing and fall back
                continue
            if 'geometry' in el:
                coords = [(pt['lon'], pt['lat']) for pt in el['geometry']]
                geom = {'type': 'Polygon', 'coordinates': [coords]}
            if geom:
                features.append({
                    'type': 'Feature',
                    'properties': {'name': el['tags'].get('name')},
                    'geometry': geom
                })
        fc = {'type': 'FeatureCollection', 'features': features}
        gdf = gpd.GeoDataFrame.from_features(fc)
        gdf['area_m2'] = gdf.geometry.to_crs(epsg=3857).area
        gdf.to_file(str(cache), driver='GeoJSON')
        return gdf
    except Exception:
        LOG.warning('Overpass fetch failed, falling back to local file')
        fallback = Path(__file__).parent / 'fallback_districts.geojson'
        return gpd.read_file(str(fallback))

if __name__ == '__main__':
    import sys
    names = [
        "Cidade Vella/Centro","Ensanche-Juan Flórez","Monte Alto","Riazor-Orzán",
        "Os Mallos-Sagrada Familia","Cuatro Caminos","Os Castros","Eirís",
        "Os Rosales","Matogrande/Palavea","A Grela"
    ]
    out = Path('data/mock/output/districts.geojson')
    out.parent.mkdir(parents=True, exist_ok=True)
    gdf = fetch_district_polygons(names, out)
    gdf.to_file(str(out), driver='GeoJSON')
    print('Saved', out)
