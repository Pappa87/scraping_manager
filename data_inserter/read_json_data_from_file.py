import os
import json
import tools.config as config
from os.path import isdir
from os import listdir
import random
import regex

def read_containers_output(action = None):
    container_output = config.containers_output
    containers_output_list = [os.path.join(container_output, content, "scraper_output", "data") for content in listdir(container_output) if is_data_location(os.path.join(container_output, content))]
    path_to_data_list = [listdir_fullpath(data_directory) for data_directory in containers_output_list]
    path_to_data_list = flatten(path_to_data_list)
    path_to_data_list = path_to_data_list[0:]

    random.shuffle(path_to_data_list)
    print(f'{len(path_to_data_list)} number of json will be parsed')
    for path_to_data in path_to_data_list:
        data = read_json_from_file(path_to_data)
        # name of the file looks lite: {ID]_t{timestamp} so
        data["key"] = os.path.basename(path_to_data).split("_")[0]
        if action is not None:
            action(data)


def is_data_location(path_to_dir):
    if not isdir(os.path.join(path_to_dir)): return False
    sub_directories = [content for content in listdir(path_to_dir) if isdir(os.path.join(path_to_dir, content))]
    if len(sub_directories) == 1 and "scraper_output" in sub_directories and isdir(os.path.join(path_to_dir, "scraper_output", "data")): return True
    else: return False


def read_datas_from_directory(path_to_dir):
    data = [read_json_from_file(path_to_dir) for item in listdir(path_to_dir)]
    return data


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def flatten(data_list):
    return [item for sublist in data_list for item in sublist]


iterator = 0


def read_json_from_file(path_to_write):
    global iterator
    if iterator % 1000 == 0:
        print(f'{iterator} number of json parsed already')

    with open(path_to_write, encoding='utf-8') as json_file:
        data = json.load(json_file)
        iterator += 1
        return data


from data_inserter.data_inspector import validate_data
read_containers_output(validate_data.validate_response)







