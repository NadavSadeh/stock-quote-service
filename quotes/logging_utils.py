import logging
import functools
import inspect

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        module = inspect.getmodule(func)
        logger_name = module.__name__ if module else __name__
        logger = logging.getLogger(logger_name)

        func_name = func.__name__
        logger.info(f"{func_name} [STARTED]")
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            logger.info(f"{func_name} [FINISHED]")
    return wrapper