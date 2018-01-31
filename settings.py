import os

from common.configWrapper import ConfigWrapper

# Settings
from common.elasticSearchWrapper import ElasticSearchWrapper

URL_PREFIX = "/api"
METHOD_POST = "POST"
METHOD_GET = "GET"
CACHE_TIMEOUT = 50
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE_NAME = DIR_PATH + "/settings.config"
cwd = os.getcwd()

LOGS_DIR = DIR_PATH + "/logs"
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = LOGS_DIR + "/paas.log"

config = ConfigWrapper(SETTINGS_FILE_NAME)
elasticSearchWrapper = ElasticSearchWrapper(configurations=config.loadElasticSearchConfigurations())

# Schema
SCHEMA = {
    "type": "object",
    "properties": {
        "pokadex_id": {"type": "number", "minimum": 1, "multipleOf": 1},
        "level": {"type": "number"},
        "name": {"type": "string"},
        "nickname": {"type": "string"},
        "type": {"type": "string"},
        "skills":
            {
                "type": "array",
                "items": {"type": "string",
                          "enum": ["ELECTRIC", "GROUND", "FIRE", "WATER", "WIND", "PSYCHIC", "GRASS"]},
            },
    },
    "required": [
        "pokadex_id",
        "name",
        "nickname",
        "type",
        "skills",
    ],
}
