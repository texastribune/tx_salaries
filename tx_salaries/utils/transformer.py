import hashlib
from StringIO import StringIO

from csvkit import convert
from csvkit.unicsv import UnicodeCSVReader
from django.core import exceptions

from .transformers import TRANSFORMERS


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
