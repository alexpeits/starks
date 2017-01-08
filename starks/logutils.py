"""

logutils
~~~~~~~~

Various logging utilities

"""

import logging
import inspect


def create_logger(*args, **kwargs):
    """Return a logger with a nicely formatted name, depending on the caller.

    This works by using inspect to grab the frame containing information
    about the caller of this function. This frame contains the module name,
    and also the class, function or method names, if any.

    """
    frame_caller = inspect.stack()[1][0]
    location = module = inspect.getmodule(frame_caller).__name__
    _, _, _, loc = inspect.getargvalues(frame_caller)
    obj = loc.get('self', None)  # check if called inside a class
    if obj is not None:
        location = '.'.join([module, obj.__class__.__name__])

    del frame_caller  # to avoid leak

    logger = logging.getLogger(location)
    return logger
