from abc import ABCMeta, abstractmethod
import yaml
import json
from os.path import splitext, exists
from utils.utility import Utility as u


class AbstractConfig(object):
    __metaclass__ = ABCMeta

    def __init__(self, conf_dict):
        self.__dict__.update(conf_dict)

    @abstractmethod
    def convert(self, format_type):
        pass

    @abstractmethod
    def get(self, prop):
        pass


class Config(AbstractConfig):
    def get(self, query_str, delimiter='.'):
        """
        Used to search internal dict for properties and make accessing
        properties more aesthetic
        Args:
            query_str (string): The key to search for in the dict where the
                                delimiter denotes nested dicts e.g.:
                                Config.get('STORAGE.DB').
        Returns:
            mixed: Value if found, None otherwise
        """
        obj = self.__dict__
        query_str = query_str.split(delimiter)

        for item in query_str:
            obj = u.dict_search(obj, item)

        return obj

    def convert(self, format_type):
        pass


class AbstractFileParser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_dict(self):
        pass


class YamlParser(AbstractFileParser):
    def __init__(self, file_path):
        """
        :type file_path: str
        """
        assert isinstance(file_path, str)
        self.__file_path = file_path

    def get_dict(self):
        """
        :rtype : dict
        """
        return dict(yaml.load(open(self.__file_path)))


class JSONParser(AbstractFileParser):
    def __init__(self, file_path):
        """
        :type file_path: basestring
        """
        assert isinstance(file_path, str)
        self.__file_path = file_path

    def get_dict(self):
        """
        :rtype : dict
        """
        return dict(json.load(open(self.__file_path)))


class ConfigFactory:
    @staticmethod
    def create(config_paths):
        """
        Args:
            config_paths (list): List of files to read. Files are read in order
                               and properties are overwritten as they appear in
                               the files
        Returs:
            Config: The Config object with the configuration settings set as
                    static attrs
        """
        target_dict = {}

        for path in config_paths:
            if exists(path):
                ext = splitext(path)[1].lower()

                if ext == '.json':
                    target_dict.update(JSONParser(path).get_dict())
                elif ext == '.yml':
                    target_dict.update(YamlParser(path).get_dict())
                else:
                    raise TypeError('Unknown Factory.')
            else:
                raise TypeError('! Invalid config path')

        return Config(target_dict)
