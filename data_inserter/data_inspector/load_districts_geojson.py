import geopandas


def transform_district(location: str):
    return location.partition(".")[0]


districts = geopandas.read_file("./data/districts.geojson")
districts = districts.to_crs(epsg=3035)

districts['coords'] = districts['geometry'].apply(lambda x: x.representative_point().coords[:])
districts['coords'] = [coords[0] for coords in districts['coords']]
districts['district'] = districts["display_name"].apply(transform_district)

