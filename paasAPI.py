import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask import jsonify
from flask_cache import Cache

from common.inputValidator import validateJsonSchema
from settings import *

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route(URL_PREFIX + "/create", methods=[METHOD_POST])
@validateJsonSchema(schema=SCHEMA)
def createNewPokemon():
    d = "ok"
    return jsonify(d)


@app.route(URL_PREFIX + "/log_test", methods=[METHOD_GET])
def logTest():
    app.logger.error("An error occurred")


@app.route(URL_PREFIX + "/cache_test/<string:a>", methods=[METHOD_GET])
@cache.cached(timeout=CACHE_TIMEOUT)
def cacheTest(a):
    print("cacheTest_" + a)
    return "cacheTest_" + a


@app.errorhandler(404)
def pageNotFound(error):
    return jsonify(message="End Point Not Found"), 404


@app.errorhandler(400)
def badRequest(error):
    return jsonify(message=error.name, errors=error.description), 400


if __name__ == "__main__":
    handler = RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
