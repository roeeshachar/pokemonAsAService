import os
import traceback

from common.configWrapper import ConfigWrapper

# Settings
from common.elasticSearchWrapper import ElasticSearchWrapper, ElasticSearchNotFoundError

# Http Consts
METHOD_POST = "POST"
METHOD_GET = "GET"
STATUS_CODE_CREATED = 201
STATUS_CODE_OK = 200
STATUS_CODE_INTERNAL_ERROR = 500
STATUS_CODE_NOT_FOUND = 404
STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_CONFLICT = 409

URL_PREFIX = "/api"
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
POKADEX_ID_FIELD = "pokadex_id"
SCHEMA = {
    "type": "object",
    "properties": {
        POKADEX_ID_FIELD: {"type": "number", "minimum": 1, "multipleOf": 1},
        "level": {"type": "number"},
        "name": {"type": "string"},
        "nickname": {"type": "string"},
        "type": {"type": "string", "enum": ["ELECTRIC", "GROUND", "FIRE", "WATER", "WIND", "PSYCHIC", "GRASS"]},
        "skills":
            {
                "type": "array",
                "items": {"type": "string"},
            },
    },
    "required": [
        POKADEX_ID_FIELD,
        "name",
        "nickname",
        "type",
        "skills",
    ],
    "additionalProperties": False,
}


def exceptionToString(e: BaseException):
    return "{type}:{message}\n{trace}".format(type=type(e), message=str(e), trace=traceback.format_exc())
