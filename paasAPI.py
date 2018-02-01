import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask import jsonify
from flask import request
from flask_caching import Cache
from werkzeug.exceptions import abort

from common.inputValidator import validateJsonSchema
from settings import *

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route(URL_PREFIX + "/create", methods=[METHOD_POST])
@validateJsonSchema(schema=SCHEMA)
def createNewPokemon():
    jsonObject = request.get_json()
    pokadexId = jsonObject[POKADEX_ID_FIELD]
    if elasticSearchWrapper.exists(documentId=pokadexId):
        return jsonify(message="Pokemon Already Exists With Given Pokadex Id", id=pokadexId,
                       success=False), STATUS_CODE_CONFLICT

    try:
        elasticSearchWrapper.create(body=jsonObject, documentId=pokadexId)
        pokemonDocument = elasticSearchWrapper.get(documentId=pokadexId)
        return jsonify(message="Pokemon Created", pokemon=pokemonDocument, success=True), STATUS_CODE_CREATED
    except BaseException as e:
        app.logger.error(exceptionToString(e))
        return jsonify(message="Error Creating Pokemon",
                       success=False), STATUS_CODE_INTERNAL_ERROR


@app.route(URL_PREFIX + "/autocomplete/<string:prefix>", methods=[METHOD_GET])
@cache.cached(timeout=CACHE_TIMEOUT)
def autoComplete(prefix: str):
    results = elasticSearchWrapper.getByPrefix(prefix=prefix)
    return jsonify(results), STATUS_CODE_OK


@app.route(URL_PREFIX + "/get/<int:id>", methods=[METHOD_GET])
def getPokemon(id: int):
    try:
        pokemon = elasticSearchWrapper.get(documentId=id)
        return jsonify(pokemon=pokemon, success=True), STATUS_CODE_OK
    except ElasticSearchNotFoundError as e:
        return jsonify(message="No Pokemon With Given Pokadex Id", id=id,
                       success=False), STATUS_CODE_NOT_FOUND


@app.errorhandler(STATUS_CODE_NOT_FOUND)
def pageNotFound(error):
    return jsonify(message="End Point Not Found"), STATUS_CODE_NOT_FOUND


@app.errorhandler(STATUS_CODE_BAD_REQUEST)
def badRequest(error):
    return jsonify(message=error.name, errors=error.description, success=False), STATUS_CODE_BAD_REQUEST


@app.errorhandler(STATUS_CODE_INTERNAL_ERROR)
def internalError(error):
    try:
        exception = error.description  # chained exception
    except AttributeError as e:
        exception = error
    app.logger.error(exceptionToString(exception))
    return jsonify(message="Internal Error Occurred", success=False), STATUS_CODE_INTERNAL_ERROR


if __name__ == "__main__":
    handler = TimedRotatingFileHandler(LOG_FILE, when="d", backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
