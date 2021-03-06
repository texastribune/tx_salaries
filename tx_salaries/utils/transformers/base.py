from copy import copy
import hashlib
import re

from .. import cleaver

DEFAULT_DATA_TEMPLATE = {
    'tx_people.Person': {},
    'tx_people.Organization': {},
    'tx_people.Post': {},
    'tx_people.Membership': {},
    'tx_people.Race': {},
    'tx_people.Links': {},
    'compensations': [{
        'tx_salaries.CompensationType': {},
        'tx_salaries.Employee': {},
    }]
}


class BaseTransformedRecord(object):
    REJECT_ALL_IF_INVALID_RECORD_EXISTS = True

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
        # Error if one of required as_dict attributes is not available
        raise AttributeError("{key} is unknown. Are all of its attributes "
                             "available?".format(key=key))

    # TODO: Test
    def get_raw_name(self):
        name_fields = [getattr(self, a) for a in self.NAME_FIELDS]
        return u' '.join(name_fields)

    # TODO: Test
    # Helper function for GenericPersonMixin
    def get_name(self):
        return self.get_cleavered_name().parse()

    # TODO: Test
    def get_cleavered_name(self):
        return self.get_name_cleaver()(self.get_raw_name())

    # TODO: Test
    def get_name_cleaver(self):
        return cleaver.EmployeeNameCleaver

    def as_dict(self):

        # Build the structured record with the required attributes
        d = copy(DEFAULT_DATA_TEMPLATE)
        d['original'] = self.data

        d['tx_people.Identifier'] = self.identifier
        d['tx_people.Person'] = self.person
        d['tx_people.Organization'] = self.organization
        d['tx_people.Post'] = self.post
        d['tx_people.Membership'] = self.membership
        d['tx_people.Race'] = self.race
        d['tx_people.Links'] = self.links
        d['compensations'] = self.compensations
        d['date_provided'] = self.DATE_PROVIDED
        return d


def create_hash_for_record(record, exclude=None):
    """
    Returns a hash for a record to be used as its identifier.

    This takes a dictionary called ``record`` and turns it into a SHA-1
    hash while excluding any fields that might vary (such as pay rate).
    Each data source is responsible for determining what fields are
    unique and immutable.

    This hash is used for tracking an employee from one import to the
    next.
    """

    data_for_hash = copy(record)
    if exclude:
        for key in exclude:
            del data_for_hash[key]

    hash_string = re.sub(u'[\s.,-]', u'', u"::".join(data_for_hash.values()))
    return hashlib.sha1(hash_string.encode('utf-8')).hexdigest()


def generic_transform(labels, source, record_class):
    """
    General purpose transform function that is provided the record_class

    To use this, provide a ``record_class`` for a given
    ``TransformedRecord``.  Note that this can not be used directly
    as a transform function as it takes three parameters, not two.  It
    is meant to be used to build a transform function and is normally
    used directly via ``transform_factory``.
    """
    data = []
    warnings = []
    for raw_record in source:
        record = record_class(dict(zip(labels, raw_record)))
        if record.is_valid:
            data.append(record.as_dict())
        else:
            warnings.append("WARNING: RECORD INVALID; {0}".format(record.data))
    if warnings and record_class.REJECT_ALL_IF_INVALID_RECORD_EXISTS:
        raise ValueError("Aborting the transformation because invalid records exist,"
                         "and there is no override to accept invalid records."
                         "{0}".format(['\n'.join(warnings)]))
    return data, warnings


def generic_merge_cell_transform(labels, source, record_class):
    """
    General purpose transform function for data sources with merge-cells

    Spreadsheets with merge cells, such as those provided by the Texas
    Tech System, require that data from the previous row be merged into
    the new row.  The CSV reader that we currently use can not handle
    these rows, so we must do it ourselves.
    """
    data = []
    last_row = None
    warnings = []
    for raw_row in source:
        row = dict(zip(labels, raw_row))
        if not raw_row[0].strip() and last_row:
            for key, value in last_row.items():
                if not row[key]:
                    row[key] = last_row[key]

        record = record_class(row)
        if record.is_valid:
            data.append(record.as_dict())
        else:
            warnings.append("WARNING: RECORD INVALID; {0}".format(record.data))
        last_row = row
    if warnings and record_class.REJECT_ALL_IF_INVALID_RECORD_EXISTS:
        raise ValueError("Aborting the transformation because invalid records exist,"
                         "and there is no override to accept invalid records.\n"
                         "{0}".format(['\n'.join(warnings)]))
    return data, warnings


def transform_factory(record_class, transform_func=None):
    """
    Simple factory for building a generic transformmer

    The second argument is used as the actual transform function, if
    provided, otherwise this dispatches to ``generic_transform``.  The
    provided ``transform_func`` is supposed to take three arguments,
    the ``labels`` and ``source`` that a transform function is supposed
    to take, along with a ``record_class`` argument that specifies which
    class is supposed to be used.
    """

    if transform_func is None:
        transform_func = generic_transform

    def transform(labels, source):
        return transform_func(labels, source, record_class=record_class)
    return transform
