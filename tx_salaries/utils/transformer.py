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
        raise exceptions.ImproperlyConfigured()


def summarize_import(organizations, filename):
    from csv import DictWriter
    columns = (
        'Name',
        'Title',
        'Department',
        'Gender',
        'Ethnicity',
        'Hire_date',
        'Tenure',
        'Annual_salary',
        'Entity',
    )

    member_kwargs = (
        'person__name',
        'post__label',
        'organization__name',
        'person__gender',
        'person__races__name',
        'employee__hire_date',
        'employee__tenure',
        'employee__compensation',
        'organization__parent__name'
    )

    outfile = open(filename, 'w')
    writer = DictWriter(outfile, columns)
    writer.writerow(dict(zip(columns, columns)))

    for org in organizations:
        employee_values = org.members.values(*member_kwargs).distinct()
        for val in employee_values:
            writer.writerow({
                'Name': val[member_kwargs[0]],
                'Title': val[member_kwargs[1]],
                'Department': val[member_kwargs[2]],
                'Gender': val[member_kwargs[3]],
                'Ethnicity': val[member_kwargs[4]],
                'Hire_date': val[member_kwargs[5]],
                'Tenure': val[member_kwargs[6]],
                'Annual_salary': val[member_kwargs[7]],
                'Entity': val[member_kwargs[8]]
            })

    outfile.close()
    print "Created %s" % filename
