from copy import copy
import hashlib
from StringIO import StringIO

from csvkit import convert
from csvkit.unicsv import UnicodeCSVReader
from django.core import exceptions


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


DEFAULT_DATA_TEMPLATE = {
    'tx_people.Person': {},
    'tx_people.Organization': {},
    'tx_people.Post': {},
    'tx_people.Membership': {},
    'tx_salaries.CompensationType': {},
    'tx_salaries.Employee': {},
}


def alamo_colleges(labels, source):
    data = []
    for raw_row in source:
        # Check to see if the row contains a status column as those are
        # always included in a valid record.  This ignores various theh
        if len(raw_row[2].strip()) is 0:
            continue

        row = dict(zip(labels, raw_row))
        d = copy(DEFAULT_DATA_TEMPLATE)
        d["original"] = raw_row
        d["tx_people.Person"] = {
            "family_name": row["Last Name"],
            "given_name": row["First Name"],
            "name": "%s %s" % (row["First Name"], row["Last Name"]),
        }

        d["tx_people.Organization"] = {
            "label": row["Department"],
        }

        d["tx_people.Post"] = {
            "label": row["Position Title"],
        }

        d["tx_people.Membership"] = {
            "start_date": row["Hire Date"],
        }

        d["tx_salaries.CompensationType"] = {
            "name": "%s Time" % "Part" if row["FT or PT Status"] == "PT" else "Full",
        }

        if row["Hourly Rate"].strip():
            compensation_key = "Hourly Rate"
        else:
            compensation_key = "FT  or PT Semester Salary"
        d["tx_salaries.Employee"] = {
            "hire_date": row["Hire Date"],
            "compensation": row[compensation_key],
        }
        data.append(d)
    return data


def brownsville_isd(labels, source):
    data = []
    for raw_row in source:
        # Brownsville likes to include the employee count as a row by
        # itself.  No need to process that.
        if raw_row[0].strip() == "EMPLOYEE COUNT:":
            continue

        row = dict(zip(labels, raw_row))
        d = copy(DEFAULT_DATA_TEMPLATE)
        d["original"] = raw_row
        d["tx_people.Person"] = {
            "family_name": row["LAST NAME"],
            "given_name": row["FIRST NAME"],
            "name": "%s %s %s" % (row["FIRST NAME"], row["MI"],
                    row["LAST NAME"]),
        }

        d["tx_people.Organization"] = {
            "label": row["CAMPUS/DEPT"],
        }

        d["tx_people.Post"] = {
            "label": row["POSITION"],
        }

        d["tx_people.Membership"] = {
            "start_date": row["HIRE_DATE"],
        }

        d["tx_salaries.CompensationType"] = {
            "name": "Full Time Teacher",
        }

        d["tx_salaries.Employee"] = {
            "hire_date": row["HIRE_DATE"],
            "compensation": row["SALARY"],
        }
        data.append(d)
    return data


def collin_college(labels, source):
    data = []
    for raw_row in source:
        row = dict(zip(labels, raw_row))
        d = copy(DEFAULT_DATA_TEMPLATE)

        job_title = row["JOB TITLE"].strip()
        compensation_type = "Full Time"
        if job_title[-2:].upper() == "PT":
            compensation_type = "Part Time"
            job_title = job_title[:-2].strip()

        # Clean up any issues with the "- PT" suffix, but do it by
        # splitting on "-" to ensure that we catch as many as possible
        split_department = row['DEPARTMENT'].split('-')[:-1]
        department = '-'.join([a.strip() for a in split_department])

        d["original"] = raw_row
        d["tx_people.Person"] = {
            "family_name": row["LAST NAME"],
            "given_name": row["FIRST NAME"],
            "name": "%s %s" % (row["FIRST NAME"], row["LAST NAME"]),
            "gender": row["SEX"],
        }
        d["tx_people.Organization"] = {
            "label": "Collin College",
            "children": [{
                "label": department,
            }],
        }

        d["tx_people.Post"] = {
            "label": job_title,
        }

        d["tx_people.Membership"] = {
            "start_date": row["CURRENT HIRE DATE"],
        }

        compensation = row["ANNUAL SALARY (HOURLY RATE FOR PT)"]
        compensation
        if compensation == 'See "Explanations" tab':
            if row["JOB TITLE"] == "Assoc Professor":
                compensation = "719"
                compensation_type = "Part Time Associate Professor"
            else:
                compensation = None
        d["tx_salaries.CompensationType"] = {
            "name": compensation_type
        }

        d["tx_salaries.Employee"] = {
            "hire_date": row["CURRENT HIRE DATE"],
            "compensation": compensation,
        }
        data.append(d)
    return data

TRANSFORMERS = {
    'ddd655aafc883a905a0e2b3556c0e42b34f21d04': [alamo_colleges, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college, ],
}
