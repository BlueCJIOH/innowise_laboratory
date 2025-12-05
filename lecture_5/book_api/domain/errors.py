class BaseDomainException(Exception):
    pass


class BookNotFound(BaseDomainException):
    pass


class InvalidBookData(BaseDomainException):
    pass