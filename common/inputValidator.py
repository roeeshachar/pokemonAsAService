from functools import wraps

from flask import request, abort
from jsonschema import Draft4Validator


class InputValidator(object):
    MISSING = "missing"

    def __init__(self, schema: dict):
        self.validator = Draft4Validator(schema=schema)

    def getValidationErrors(self, instance: dict):
        errors = {}
        for err in self.validator.iter_errors(instance=instance):
            message = err.message
            path = err.path
            if len(path) == 0:
                if self.MISSING not in errors:
                    errors[self.MISSING] = []

                errors[self.MISSING].append(message)

            else:
                errors[path[0]] = message

        return errors


def validateJsonSchema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            jsonObject = request.get_json()
            inputValidator = InputValidator(schema=schema)
            errors = inputValidator.getValidationErrors(instance=jsonObject)
            if errors:
                abort(400, errors)

            return func(*args, **kwargs)

        return wrapper

    return decorator
