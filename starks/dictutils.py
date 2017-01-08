"""

dictutils
~~~~~~~~~

Dictionary utilities

"""

import sys
from copy import deepcopy
from itertools import chain
from collections import Hashable

_PY3 = sys.version_info[0] == 3


def _check_valid_doubledict(values):
    """Check if double dict values are unique and hashable."""
    seen = set()
    for value in values:
        if not isinstance(value, Hashable):
            raise ValueError('DoubleDict values must be hashable')
        if value in seen:
            raise ValueError('DoubleDict values must be unique')
        seen.add(value)


def _check_update_doubledict(args, kwargs, dd):
    seen_k = set(dd._keys())
    seen_v = set(dd._values())
    kw_items = kwargs.items() if _PY3 else kwargs.iteritems()
    arg_items = chain.from_iterable(args)
    for k, v in chain(arg_items, kw_items):
        if not isinstance(v, Hashable):
            raise ValueError('DoubleDict values must be hashable')
        if k not in seen_k:
            if v in seen_v:
                raise ValueError('DoubleDict values must be unique')
        else:
            if v in seen_v and dd[k] != v:
                raise ValueError('DoubleDict values must be unique')
        seen_k.add(k)
        seen_v.add(v)


class DoubleDict(dict):
    """Dictionary that enables reverse lookup.

    >>> dd = DoubleDict([('a', 1), ('b', 2), ('c', 3)])
    >>> dd == {'a': 1, 'b':2, 'c': 3}
    True
    >>> dd.reverse == {1: 'a', 2: 'b', 3: 'c'}
    True

    For this to work, dict values must be unique and hashable:

    >>> dd = DoubleDict([('a', 1), ('b', 2), ('c', 1)])
    Traceback (most recent call last):
    ...
    ValueError: DoubleDict values must be unique
    >>>
    >>> dd = DoubleDict([('a', 1), ('b', 2), ('c', {'foo': 'bar'})])
    Traceback (most recent call last):
    ...
    ValueError: DoubleDict values must be hashable

    DoubleDict.reverse is lazy, and also returns a DoubleDict.

    """

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError('DoubleDict expected at most 1 arguments, got 2')
        super(DoubleDict, self).__init__(*args, **kwargs)

        self._keys = self.keys if _PY3 else self.iterkeys
        self._values = self.values if _PY3 else self.itervalues
        self._items = self.items if _PY3 else self.iteritems

        _check_valid_doubledict(self._values())

    def _copyitems(self):
        """Yield deep copies of keys and values."""
        for k, v in self._items():
            yield deepcopy(k), deepcopy(v)

    @property
    def reverse(self):
        """Return a DoubleDict with reverse mapping."""
        return DoubleDict({v: k for k, v in self._copyitems()})

    @reverse.setter
    def reverse(self, value):
        raise AttributeError('DoubleDict.reverse cannot be set')

    def __setitem__(self, item, value):
        if not isinstance(value, Hashable):
            raise ValueError('DoubleDict values must be hashable')
        if item not in self._keys():
            if value in self._values():
                raise ValueError('DoubleDict values must be unique')
        else:
            if value in self._values() and self[item] != value:
                raise ValueError('DoubleDict values must be unique')
        super(DoubleDict, self).__setitem__(item, value)

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError('DoubleDict.update expected at most'
                            '1 arguments, got 2')
        _check_update_doubledict(args, kwargs, self)
        super(DoubleDict, self).update(*args, **kwargs)

    def __repr__(self):
        dict_repr = super(DoubleDict, self).__repr__()
        return 'DoubleDict({})'.format(dict_repr)
