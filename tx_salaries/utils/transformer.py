import hashlib
from StringIO import StringIO

from csvkit import convert
from csvkit.unicsv import UnicodeCSVReader
from django.core import exceptions

from .transformers import TRANSFORMERS


def convert_to_csv_reader(filename, sheet=None):
    format = convert.guess_format(filename)
    f = open(filename, "rb")
    convert_kwargs = {}
    if sheet is not None:
        # Only pass `sheet` to the `convert` function when its set to
        # a non-None value.  This is done to satisfy csvkit which checks
        # for the presence of `sheet`, not whether it's valid.
        convert_kwargs['sheet'] = sheet
    converted = StringIO(convert.convert(f, format, **convert_kwargs))
    reader = UnicodeCSVReader(converted)
    return reader


def transform(filename, sheet=None, label_row=1):
    reader = convert_to_csv_reader(filename, sheet=sheet)
    for i in range(1, int(label_row)):
        reader.next()
    labels = reader.next()
    transformers = get_transformers(labels)

    if len(transformers) > 1:
        question = 'Which transformer would you like to use?\n'
        for i in range(0, len(transformers)):
            try:
                question += '%i: %s\n' % (i, transformers[i][0])
            except TypeError:
                raise Exception("Please list transformers with identical hashes as tuples")
        transformer_choice = int(input(question))
        transformer = transformers[transformer_choice][1]

    else:
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
        raise exceptions.ImproperlyConfigured("There are no transformers that match the header labels of this file")
