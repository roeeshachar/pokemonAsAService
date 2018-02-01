from typing import List

from common.elasticSearchConfigurations import ElasticSearchConfigurations
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError as ElasticSearchNotFoundError


class ElasticSearchWrapper(object):
    SOURCE = "_source"
    HITS = "hits"
    TEXT = "text"
    PROPERTIES = "properties"
    MAPPING = "mappings"

    def __init__(self, configurations: ElasticSearchConfigurations):
        self.configurations = configurations
        self.es = Elasticsearch(
            hosts=[{'host': self.configurations.host, 'port': self.configurations.port}],
        )

    def create(self, body: dict, documentId):
        ans = self.es.create(index=self.configurations.index, doc_type=self.configurations.docType, body=body,
                             id=documentId)
        return ans

    def exists(self, documentId):
        return self.es.exists(index=self.configurations.index, doc_type=self.configurations.docType, id=documentId)

    def get(self, documentId):
        try:
            return self.es.get_source(index=self.configurations.index, doc_type=self.configurations.docType,
                                      id=documentId)
        except ElasticSearchNotFoundError as e:
            raise e

    @classmethod
    def constructPrefixFieldQuery(cls, fields: List[str], prefix: str):
        prefixes = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "prefix": {
                                field: prefix,
                            }
                        } for field in fields
                        ]
                }
            }
        }

        return prefixes

    def getByPrefix(self, prefix: str):
        try:
            textFields = self.getTextFields()
            ans = self.es.search(index=self.configurations.index, doc_type=self.configurations.docType,
                                 body=self.constructPrefixFieldQuery(fields=textFields, prefix=prefix))
            return [elm[self.SOURCE] for elm in ans[self.HITS][self.HITS]]
        except ElasticSearchNotFoundError as e:
            raise e

    def getTextFields(self):
        mapping = self.getMapping()
        return [k for k, v in
                mapping[self.configurations.index][self.MAPPING][self.configurations.docType][self.PROPERTIES].items()
                if v["type"] == "text"]

    def getMapping(self) -> dict:
        return self.es.indices.get_mapping(index=self.configurations.index, doc_type=self.configurations.docType)
