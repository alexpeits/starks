"""

perfutils
~~~~~~~~~

Utilities for measuring performance

"""

from __future__ import print_function

from time import time as _time
from contextlib import contextmanager as _contextmanager


@_contextmanager
def timer(block_name='block'):
    """Context manager that prints the execution time of a block.

    Usage:

    >>> with timer('squared_ints'):
    ...     _ = [i ** 2 for i in xrange(10000000)]

    >>> with timer():
    ...     _ = [i ** 2 for i in xrange(100000000)]

    """
    start = _time()
    try:
        yield
    finally:
        lapse = _time() - start
        print('({:12.12} {:7.4} s)'
              .format(block_name, lapse))
