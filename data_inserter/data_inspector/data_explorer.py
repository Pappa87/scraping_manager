import json


# you have to run this function on every read data get a bunch of information that help data cleaning and validation
def explore_data(data: dict):
    extend_attriube_list_with_data(data)


def write_result_to_file():
    data = {}
    data["attribute"] = attribute_list
    with open('C:\\tmp\\json_result\\result.json', 'w') as outfile:
        json.dump(data, outfile)


attribute_list = []


# result :
#     Ingatlan állapota x
#     Komfort x
#     Energiatanúsítvány x
#     Emelet x
#     Épület szintjei x
#     Lift x
#     Belmagasság x
#     Fűtés x
#     Akadálymentesített x
#     Fürdő és WC x
#     Tájolás X
#     Kilátás x
#     Kertkapcsolatos x
#     Tetőtér x
#     Parkolás x
#     Alapterület X
#     Szobák száma x
#     Ár x
#     description x
#     location x
#     time_stamp
#     Erkély x
#     Építés éve x
#     Légkondicionáló x
#     Rezsiköltség x
#     Parkolóhely ára x
#     Panelprogram x
#     Lakópark neve x
#     Pince
#     Telekterület
#     no  key, it is the name of the file
#     no number of images, not needed
def extend_attriube_list_with_data(data: dict):
    for attribute in data.keys():

        # if there is € the attribute consists the Ár
        if "€" in attribute: return
        if attribute not in attribute_list: attribute_list.append(attribute)


