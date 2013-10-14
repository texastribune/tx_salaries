from copy import copy
import hashlib
import re

DEFAULT_DATA_TEMPLATE = {
    'tx_people.Person': {},
    'tx_people.Organization': {},
    'tx_people.Post': {},
    'tx_people.Membership': {},
    'compensations': [{
        'tx_salaries.CompensationType': {},
        'tx_salaries.Employee': {},
    }]
}


class BaseTransformedRow(object):
    def __init__(self, data=None, **kwargs):
        self.data = data

    def __getattr__(self, key):
        if key in self.MAP:
            return self.MAP[key]
        else:
            actual_key = "{key}_key".format(key=key)
            if actual_key in self.MAP:
                return self.data[self.MAP[actual_key]]

        raise AttributeError("{key} is unknown".format(key=key))


def create_hash_for_row(row, exclude=None):
    """
    Returns a hash for a row to be used as its identifier.

    This takes a dictionary called ``row`` and turns it into a SHA-1
    hash while excluding any fields that might vary (such as pay rate).
    Each data source is responsible for determining what fields are
    unique and immutable.

    This hash is used for tracking an employee from one import to the
    next.
    """

    data_for_hash = copy(row)
    if exclude:
        for key in exclude:
            del data_for_hash[key]

    hash_string = re.sub('[\s.,-]', '', "::".join(data_for_hash.values()))
    return hashlib.sha1(hash_string).hexdigest()
