"""

iterutils
~~~~~~~~~

Utilities for containers and iteration

"""


def sort_by(lists, keylist, reverse=False):
    """Sort the provided args (lists or tuples) according to the key.

    Args:
        lists: list of lists or tuples to be sorted
        keylist: list that will dictate the sorting
        reverse: True or False

    Returns:
        list of sorted lists

    Usage:

    >>> sort_by([[3, 4, 2, 6], ['a', 'k', 'o', 'p']], [1, 3, 2, 0])
    [[6, 3, 2, 4], ['p', 'a', 'o', 'k']]

    """
    combined = zip(keylist, *lists)
    sort_comb = sorted(combined, key=lambda x: x[0], reverse=reverse)
    return [list(i) for i in zip(*sort_comb)[1:]]
