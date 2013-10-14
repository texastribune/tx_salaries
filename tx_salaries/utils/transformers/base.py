from copy import copy
import hashlib
import re

from .. import cleaver

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

    def get_mapped_value_key(self, key):
        return self.MAP[key[:-4]]

    def get_mapped_value(self, key):
        return self.data[self.MAP[key]]

    def is_mapped_value_key(self, key):
        return key[-4:] == '_key' and key[:-4] in self.MAP

    def is_mapped_value(self, key):
        return key in self.MAP and self.MAP[key] in self.data

    def __getattr__(self, key):
        if self.is_mapped_value_key(key):
            return self.get_mapped_value_key(key)
        elif self.is_mapped_value(key):
            return self.get_mapped_value(key)
        raise AttributeError("{key} is unknown".format(key=key))

    # TODO: Test
    def get_name(self):
        return cleaver.EmployeeNameCleaver(self.raw_name).parse()


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
