import json
import regex


def get_GPS_from_script(script: str):
    geojson = extract_geojson(script)
    GPS = get_GPS_from_geojson(geojson)
    return GPS


def extract_geojson(script: str):
    start_index = script.find("""{"type":"FeatureCollection""")
    json_left_side_removed = script[start_index:]

    json_string = find_first_json_in_text(json_left_side_removed)
    geojson = json.loads(json_string)
    return geojson


pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')


def find_first_json_in_text(text):
    global pattern
    first_json = pattern.search(text).group()
    print(first_json)
    return first_json


def get_GPS_from_geojson(geojson):
    features = geojson["features"]
    first_entity = features[0]
    second_entity = features[1]

    # return first_entity["geometry"]
    if second_entity["name"] == '-':
        # print(first_entity["name"])
        return second_entity["geometry"]
    else:
        # print(first_entity["name"] + " " + second_entity["name"])
        return first_entity["geometry"]


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
    print(result)
    return result
