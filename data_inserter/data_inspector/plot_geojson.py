import matplotlib.pyplot as plt
import geopandas
import contextily as ctx


def plot_district_zoom(district, geojson):
    from data_inserter.data_inspector.load_districts_geojson import districts
    districts = districts[districts["district"] == district]
    geo_dataframe = geopandas.GeoDataFrame.from_features(geojson['features'])

    f, ax = plt.subplots(1, figsize=(12, 12))
    districts = districts.to_crs(epsg=3857)
    districts.plot(ax=ax, alpha=0.2)

    # geo_dataframe.crs = 'WGS84'
    geo_dataframe.crs = "epsg:4326"
    geo_dataframe = geo_dataframe.to_crs(epsg=3857)
    geo_dataframe.plot(ax=ax)

    lims = plt.axis('equal')
    ax.set_facecolor('white')
    ctx.add_basemap(ax, zoom=14)
    plt.show()