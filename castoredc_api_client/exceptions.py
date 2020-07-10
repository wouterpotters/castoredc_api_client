import functools


class NotFoundException(Exception):
    pass


class CastorException(Exception):
    pass


def castor_exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arguments = list(args)
        client = arguments[0]
        try:
            client.logger.info(
                "stack: {0}".format(func)
                + " - args: {0} - kwargs: {1}".format(args, kwargs)
            )
            return func(*args, **kwargs)
        except CastorException as e:
            client.logger.exception(
                "error: "
                + str(e)
                + " stack: {0}".format(func)
                + " - args: {0} - kwargs: {1}".format(args, kwargs)
            )
            raise

    return wrapper
