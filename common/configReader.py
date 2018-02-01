import configparser
import json
import os

from typing import Any, Tuple


class ConfigReader(object):
    """
    Handles Read/Write to config files
    """
    @classmethod
    def _deserialize(cls, value: str):
        return json.loads(value)

    @classmethod
    def _serialize(cls, value: str):
        return json.dumps(value)

    @classmethod
    def _getConfigValue(cls, config: configparser.ConfigParser, section: str, key: str):
        """

        :param config:
        :param section: The section the key is in
        :param key:
        :return:
        """
        if not cls._sectionExists(config=config, section=section):
            raise Exception("Section Not Exists", section)

        keyExists, value = cls._keyExists(config=config, section=section, key=key)
        if not keyExists:
            raise Exception("Key Not Exists", key)

        return cls._deserialize(value=value)

    @classmethod
    def _addSection(cls, config: configparser.ConfigParser, section: str) -> configparser.ConfigParser:
        config.add_section(section)
        return config

    @classmethod
    def _sectionExists(cls, config: configparser.ConfigParser, section: str) -> bool:
        return section in config

    @classmethod
    def _keyExists(cls, config: configparser.ConfigParser, section: str, key: str) -> Tuple[bool, str]:
        value = config.get(section=section, option=key, fallback=None)
        return value is not None, value

    @classmethod
    def _addKeyValueMapping(cls, config: configparser.ConfigParser, section: str, key: str,
                            value: Any) -> configparser.ConfigParser:
        if not cls._sectionExists(config=config, section=section):
            config = cls._addSection(config=config, section=section)

        config[section][key] = cls._serialize(value=value)
        return config

    @classmethod
    def _saveConfig(cls, config: configparser.ConfigParser, fileName: str) -> configparser.ConfigParser:
        with open(fileName, 'w') as configfile:
            config.write(configfile)

        return config

    @classmethod
    def _touch(cls, fileName, times=None):
        with open(fileName, 'a'):
            os.utime(fileName, times)

    @classmethod
    def loadConfigParser(cls, fileName: str) -> configparser.ConfigParser:
        if not cls._fileExists(fileName):
            cls._touch(fileName=fileName)

        config = configparser.ConfigParser()
        config.read(fileName)
        return config

    @classmethod
    def _fileExists(cls, fileName: str) -> bool:
        return os.path.isfile(fileName)

    @classmethod
    def getConfigValue(cls, fileName: str, section: str, key: str):
        """

        :param fileName:
        :param section:
        :param key:
        :return:
        """
        config = cls.loadConfigParser(fileName=fileName)
        if not cls._sectionExists(config=config, section=section):
            raise Exception("Section Not Exists", section)

        keyExists, value = cls._keyExists(config=config, section=section, key=key)
        if not keyExists:
            raise Exception("Key Not Exists", key)

        return cls._deserialize(value=value)

    @classmethod
    def addSection(cls, fileName: str, section: str):
        config = cls.loadConfigParser(fileName=fileName)
        config.add_section(section)
        cls._saveConfig(config=config, fileName=fileName)

    @classmethod
    def addKeyValueMapping(cls, fileName: str, section: str, key: str,
                           value: Any):
        config = cls.loadConfigParser(fileName=fileName)
        if not cls._sectionExists(config=config, section=section):
            config = cls._addSection(config=config, section=section)

        config[section][key] = cls._serialize(value=value)
        cls._saveConfig(config=config, fileName=fileName)
