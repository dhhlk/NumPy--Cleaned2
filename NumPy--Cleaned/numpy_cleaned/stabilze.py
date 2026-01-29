from functools import lru_cache

class StabilizeError(Exception):
    """Raised when a stabilized function rule is violated."""
    pass

def stabilize(func):
    """
    Marks a function as stable, trustworthy, and safe.
    Caches repeated calls for efficiency.
    """
    cache = {}

    def wrapper(*args):
        key = tuple(args)
        if key in cache:
            return cache[key]
        try:
            result = func(*args)
        except ZeroDivisionError:
            raise StabilizeError("Cannot divide by zero. Please change the denominator.")

        cache[key] = result
        return result

    wrapper.__stablised__ = True
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper   