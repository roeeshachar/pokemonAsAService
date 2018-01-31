from common.configReader import ConfigReader
from common.elasticSearchConfigurations import ElasticSearchConfigurations


class ConfigWrapper(object):
    KEY_HOST = "host"
    KEY_PORT = "port"
    KEY_INDEX = "index"
    KEY_DOC_TYPE = "doc_type"

    SECTION_ES = "ElasticSearch"

    def __init__(self, configFileName: str):
        self.configFileName = configFileName

    def loadElasticSearchConfigurations(self) -> ElasticSearchConfigurations:
        host = ConfigReader.getConfigValue(fileName=self.configFileName, section=self.SECTION_ES, key=self.KEY_HOST)
        port = ConfigReader.getConfigValue(fileName=self.configFileName, section=self.SECTION_ES, key=self.KEY_PORT)
        index = ConfigReader.getConfigValue(fileName=self.configFileName, section=self.SECTION_ES, key=self.KEY_INDEX)
        docType = ConfigReader.getConfigValue(fileName=self.configFileName, section=self.SECTION_ES,
                                              key=self.KEY_DOC_TYPE)

        return ElasticSearchConfigurations(host=host, port=port, index=index, docType=docType)
