from data_inserter.scraped_data_into_row import response_to_orgainized_attribute_list, trim_response
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from data_inserter.data_inspector import plot_geojson
from tools import number_converter
import regex


# 28956785
def validate_response(response):
    response = trim_response(response)
    attribute_list = response_to_orgainized_attribute_list(response)
    print_attribute_list(attribute_list)

    ID = attribute_list["key"]
    district = get_disctrict(attribute_list["location"])
    geo_json = create_geosjon(ID, attribute_list["gps"])
    open_article_in_web(ID)
    plot_geojson.plot_district_zoom(district, geo_json)
    print('-----------------------------------------------------------------------')


mandatory_attributes = ["key", "Ár", "description", "location", "time_stamp", "type", "Szobák száma", "Alapterület"]

def print_attribute_list(attribute_list: dict):
    print(f'{attribute_list["key"]} : ')

    print('mantdatory attributes: ')
    for mandatory_attribute in mandatory_attributes:
        print(f"\t {mandatory_attribute} : {attribute_list[mandatory_attribute]}")

    filtered_attribute_list = [(attribute_name, attribute_value) for attribute_name, attribute_value in attribute_list.items() if attribute_value != "NA"]
    # -1 needed because gps dont appear in mandatory or optional list neither, it appears on the map
    print(f'optinal attributes size: {len(filtered_attribute_list) - len(mandatory_attributes) - 1} ')
    for attribute_name, attribute_value in filtered_attribute_list:
        if attribute_name in mandatory_attributes: continue
        if attribute_name == "gps": continue; print_geo_json(attribute_value)
        else: print(f"\t {attribute_name} : {attribute_value}")
    print("")


def print_geo_json(geo_json):
    features = geo_json["features"]
    print("\t geojson:")
    for feature in features:
        if "name" in feature:
            print(f"\t\t name : {feature['name']}")
            print(f"\t\t\t category : {feature['category']}")
            print(f"\t\t\t type : {feature['geometry']['type']}")


def get_disctrict(location):
    pattern = regex.compile(r'\d*. kerület')
    district_text = pattern.search(location).group()
    arabic_district_number = district_text.split(".")[0]
    district_number = number_converter.arabic_to_roman(arabic_district_number)
    return district_number


def create_geosjon(ID, geometry):
    result = \
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": geometry,
                "properties": {
                    "ID": ID
                }
            }
        ]
    }
    return result


driver = webdriver.Chrome(ChromeDriverManager().install())


def open_article_in_web(ID):
    url = f"https://ingatlan.com/{ID}"
    driver.get(url)
# def visialize_GPS(geo_json):
