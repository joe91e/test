from os import path
from config.cfg import ConfigFactory

config_path = path.dirname(path.abspath(__file__)) + "/../config/"

CFG_OBJ = ConfigFactory.create((
    config_path + 'default.yml',
    config_path + 'development.yml'
))
