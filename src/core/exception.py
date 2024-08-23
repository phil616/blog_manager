class APIException(Exception):
    pass


class ValidationException(APIException):
    pass


class LockException(APIException):
    pass
