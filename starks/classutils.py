"""

classutils
~~~~~~~~~~

Utilities for classes and objects

"""


class SingletonMeta(type):
    """Metaclass that provides singleton functionality.

    Usage:

    >>> class Foo(object):
    ...     __metaclass__ = SingletonMeta
    ...
    >>> a = Foo()
    >>> b = Foo()
    >>> a is b
    True

    """

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            obj = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._inst = obj
        return cls._inst


class Singleton(object):
    """Base class that adds singleton functionality to subclasses.

    Usage:

    >>> class Foo(Singleton):
    ...     pass
    ...
    >>> a = Foo()
    >>> b = Foo()
    >>> a is b
    True

    """

    _inst = None

    def __new__(cls, *args, **kwargs):
        if cls._inst is None:
            obj = super(Singleton, cls).__new__(cls, *args, **kwargs)
            cls._inst = obj
        return cls._inst


def singleton(cls):
    """Decorator that provides singleton functionality.

    >>> @singleton
    ... class Foo(object):
    ...     pass
    ...
    >>> a = Foo()
    >>> b = Foo()
    >>> a is b
    True

    """
    _inst = [None]

    def decorated(*args, **kwargs):
        if _inst[0] is None:
            _inst[0] = cls(*args, **kwargs)
        return _inst[0]
    return decorated
