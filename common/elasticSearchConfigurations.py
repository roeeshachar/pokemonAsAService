class ElasticSearchConfigurations(object):
    def __init__(self, host: str, port: int, index: str, docType: str):
        self.host = host
        self.port = port
        self.index = index
        self.docType = docType
