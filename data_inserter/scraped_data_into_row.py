import tools.config as config
from datetime import datetime
from data_inserter.gps_extractor import get_GPS_from_script, extract_geojson


def response_to_tuple(response):
    response = pre_fix_response(response)
    organized_attribute_list = response_to_orgainized_attribute_list(response)
    data_tuple = attribute_list_to_tuple(organized_attribute_list)
    return data_tuple


def pre_fix_response(response: dict):
    pre_fixed_respose = {}
    for attribute_name, attribute_value in response.items():
        trimmed_name = attribute_name.strip()
        trimmed_value = attribute_value.strip() if isinstance(attribute_value, str) else attribute_name
        pre_fixed_respose[trimmed_name] = trimmed_value

    if " Hitelre van szükséged? Kalkulálj! " in response:
        pre_fixed_respose["Ár"] = response[" Hitelre van szükséged? Kalkulálj! "]
    return pre_fixed_respose


def response_to_orgainized_attribute_list(response):
    attribute_names = config.attribut_names
    attribute_dict = {}
    for attribute_name in attribute_names:
        copy_attriubte(attribute_name, response, attribute_dict)
    copy_euro_Ar(response, attribute_dict)

    attribute_dict['time_stamp'] = transform_time_stamp(attribute_dict['time_stamp'])
    attribute_dict['gps'] = get_GPS_from_script(attribute_dict['gps'])



    return attribute_dict


def copy_attriubte(attribute, response, record):
    if attribute in response:
        record[attribute] = response[attribute]
    else:
        record[attribute] = "NA"


def copy_euro_Ar(response, record):
    for attribute, value in response.items():
        if "€" in attribute:
            record["Ár"] = value
            return


def attribute_list_to_tuple(attr_list):
    record = \
        (
            attr_list['Akadálymentesített'],
            attr_list['Alapterület'],
            attr_list['Ár'],
            attr_list['Belmagasság'],
            attr_list['description'],
            attr_list['Emelet'],
            attr_list['Energiatanúsítvány'],
            attr_list['Építés éve'],
            attr_list['Épület szintjei'],
            attr_list['Erkély'],
            attr_list['Fürdő és WC'],
            attr_list['Fűtés'],
            attr_list['Ingatlan állapota'],
            attr_list['Kertkapcsolatos'],
            attr_list['Kilátás'],
            attr_list['Komfort'],
            attr_list['Lakópark neve'],
            attr_list['Légkondicionáló'],
            attr_list['Lift'],
            attr_list['location'],
            attr_list['number of images'],
            attr_list['Panelprogram'],
            attr_list['Parkolás'],
            attr_list['Parkolóhely ára'],
            attr_list['Rezsiköltség'],
            attr_list['Szobák száma'],
            attr_list['Tájolás'],
            attr_list['Tetőtér'],
            attr_list['time_stamp'],
            attr_list['type'],
            attr_list['gps'],
            attr_list['key']
        )
    return record


def transform_time_stamp(time_stamp):
    date = datetime.strptime(time_stamp, '%Y.%m.%d. %H:%M:%S')
    return date.timestamp()





