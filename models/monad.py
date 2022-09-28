from collections.abc import Callable

from sqlalchemy.exc import OperationalError, IntegrityError
from google.api_core.exceptions import ServiceUnavailable, NotFound
import redis, requests



class RepositoryMaybeMonad:

    def __init__(self, data, error_status = None):
        self.data = data
        self.error_status = error_status

    async def bind(self, function: Callable):
        if not self.data:
            self.error_status = {"status": 500, "reason": "No data in repository monad"}
            return RepositoryMaybeMonad(None, self.error_status)
        try:
            await function(self.data)
            return RepositoryMaybeMonad(self.data, self.error_status)
        except OperationalError:
            self.error_status = {"status": 502, "reason": "Failed to connect to database"}
            return RepositoryMaybeMonad(None, self.error_status)
        except IntegrityError:
            self.error_status = {"status": 409, "reason": "Failed to insert data into database"}
            return RepositoryMaybeMonad(None, self.error_status)

class ServiceDirectoryMaybeMonad:

    def __init__(self, data, result=None, error_status=None):
        self.data = data
        self.error_status = error_status
        self.result = result

    async def bind(self, function):
        if not self.data:
            self.error_status = {"status": 500, "reason": "No data in repository monad"}
            return ServiceDirectoryMaybeMonad(None, None, self.error_status)
        try:
            self.result = await function(self.data)
            return ServiceDirectoryMaybeMonad(None, self.result, self.error_status)
        except ServiceUnavailable:
            self.error_status = {"status": 502, "reason": "Failed to connect to service directory"}
            return ServiceDirectoryMaybeMonad(None, None, self.error_status)
        except NotFound:
            self.error_status = {"status": 404, "reason": "Failed to resolve name"}
            return ServiceDirectoryMaybeMonad(None, None, self.error_status)


class RedisMaybeMonad:

    def __init__(self, key, value, error_status=None):
        self.key = key
        self.value = value
        self.error_status = error_status

    def bind(self, function):
        if not self.key or not self.value:
            self.error_status = {"status": 500, "reason": "No data in repository monad"}
            return RedisMaybeMonad(None, None, self.error_status)
        try:
            function(self.key, self.value)
            return RedisMaybeMonad(self.key, self.value, self.error_status)
        except redis.exceptions.ConnectionError:
            self.error_status = {"status": 502, "reason": "Failed to connect to redis"}
            return RedisMaybeMonad(None, None, self.error_status)

class RequestMaybeMonad:

    def __init__(self, host, json, error_status=None):
        self.host = host
        self.json = json
        self.error_status = error_status

    def bind(self, function):
        if not self.host or not self.json:
            self.error_status = {"status": 500, "reason": "No data in repository monad"}
            return RequestMaybeMonad(None, None, self.error_status)
        try:
            function(self.host, json=self.json)
            return RequestMaybeMonad(None, None, self.error_status)
        except requests.exceptions.Timeout:
            self.error_status = {"status": 502, "reason": "Downstream request timed out"}
            return RequestMaybeMonad(None, None, self.error_status)
        except requests.exceptions.RequestException as e:
            self.error_status = {"status": 502, "reason": "Request failed to connect"}
            return RequestMaybeMonad(None, None, self.error_status)