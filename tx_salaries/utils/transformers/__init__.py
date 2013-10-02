from copy import copy
import hashlib
from StringIO import StringIO

from csvkit import convert
from csvkit.unicsv import UnicodeCSVReader
from django.core import exceptions

from . import alamo_colleges
from . import brownsville_isd
from . import collin_college
from . import el_paso_county


def convert_to_csv_reader(filename):
    format = convert.guess_format(filename)
    f = open(filename, "rb")
    converted = StringIO(convert.convert(f, format))
    reader = UnicodeCSVReader(converted)
    return reader


def transform(filename):
    reader = convert_to_csv_reader(filename)
    labels = reader.next()
    transformers = get_transformers(labels)

    if len(transformers) > 1:
        raise Exception("TODO")

    transformer = transformers[0]
    # TODO: Figure out a better way to pass a dict reader in
    data = transformer(labels, reader)
    return data


def generate_key(labels):
    return hashlib.sha1("::".join(labels)).hexdigest()


def get_transformers(labels):
    """
    Return one (or more) transfer for a given set of headers

    This takes a list of headers for a given spreadsheet and returns
    the known transformers that match against it.
    """
    try:
        return TRANSFORMERS[generate_key(labels)]
    except KeyError:
        raise exceptions.ImproperlyConfigured()


TRANSFORMERS = {
    'ddd655aafc883a905a0e2b3556c0e42b34f21d04': [alamo_colleges.transform, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd.transform, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college.transform, ],
    'd18ad5c9635a40de15b0ead0e8f8fe97b8ccca31': [el_paso_county.transform, ],
}
