# Functions to create, read and write a config file
import configparser


def create_config_file():
    config = configparser.ConfigParser()
    config["LOGIN"] = {"AutomaticLogin": "0"}
    with open("config.ini", "w") as file:
        config.write(file)
    file.close()


def read_value(section, key):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config.get(section, key)


def change_value(section, key, value):
    config = configparser.ConfigParser()
    config.read("config.ini")
    config.set(section, key, value)
    with open("config.ini", "w") as file:
        config.write(file)
    file.close()
