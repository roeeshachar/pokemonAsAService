from common.elasticSearchConfigurations import ElasticSearchConfigurations
from elasticsearch import Elasticsearch


class ElasticSearchWrapper(object):
    def __init__(self, configurations: ElasticSearchConfigurations):
        self.configurations = configurations
        self.es = Elasticsearch(
            hosts=[{'host': self.configurations.host, 'port': self.configurations.port}],
        )

    def create(self, body: dict, documentId=None):
        self.es.create(index=self.configurations.index, doc_type=self.configurations.docType, body=body, id=documentId)
