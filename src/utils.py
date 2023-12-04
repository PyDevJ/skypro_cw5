import os
import json
from configparser import ConfigParser

default_path = os.path.abspath("data/database.ini")


def config(filename: str = default_path, section: str = "postgresql"):
    """
    Функция для получения параметров базы данных
    """
    path_absolute = os.path.abspath(filename)
    parser = ConfigParser()
    parser.read(path_absolute)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def load_companies(filename: str):
    """
    Функция для получения списка компаний из файла данных JSON
    """
    with open(filename, 'r', encoding='UTF-8') as file:
        result = json.load(file)
    return result
