from copy import copy
import re

from name_cleaver import cleaver, names

from .import base


regex_i = lambda a: re.compile(a, re.IGNORECASE)

DEPARTMENT_NAME_MAP = (
    (regex_i(r' OF '), ' of '),
    (regex_i(r' AT '), ' at '),
    (regex_i(r' THE '), ' the '),
    (regex_i(r'ADM\.$'), 'Administration'),
    (regex_i(r'DIST ATTY'), 'District Attorney'),
    (regex_i(r'COATTYADM'), 'County Attorney Administration'),
    (regex_i(r'COATTY'), 'County Attorney'),
    (regex_i(r'\-TAIP'), '- Treatment Alternative to Incarceration Program'),
    (regex_i(r'AP COMMUNITY INTERVENTION CTR'), 'Adult Probation Community Intervention Center'),
    (regex_i(r'ADULT PROB-GANG INTERVENTION'), 'Adult Probation - Gang Intervention'),
)


class DepartmentName(names.OrganizationName):
    def case_name_parts(self):
        super(DepartmentName, self).case_name_parts()
        self.expand_abbreviations()
        return self

    def expand_abbreviations(self):
        for pattern, replacement in DEPARTMENT_NAME_MAP:
            self.name = re.sub(pattern, replacement, self.name)


class DepartmentNameCleaver(cleaver.OrganizationNameCleaver):
    object_class = DepartmentName



def transform(labels, source):
    data = []
    for raw_row in source:
        if len(raw_row[0].strip()) is 0:
            continue

        row = dict(zip(labels, raw_row))
        d = copy(base.DEFAULT_DATA_TEMPLATE)
        d["original"] = row
        d["tx_people.Person"] = {
            "family_name": row["LAST NAME"],
            "given_name": row['FIRST NAME'],
            "name": "%s %s %s" % (row["FIRST NAME"], row['MIDDLE'],
                    row["LAST NAME"]),
        }

        department = DepartmentCleaver(row['DEPARTMENT'].title()).parse()
        d["tx_people.Organization"] = {
            "label": department,
        }

        d["tx_people.Post"] = {
            "label": row["JOB TITLE"],
        }

        d["tx_people.Membership"] = {
            "start_date": row["HIRE DATE"],
        }

        d["tx_salaries.CompensationType"] = {
            "name": "{0} Time".format("Part" if row["PART FULL"].strip() == "P"
                    else "Full"),
        }

        if row["ANNUAL RATE"].strip() == "0":
            compensation_key = "PAY RATE"
        else:
            compensation_key = "ANNUAL RATE"
        d["tx_salaries.Employee"] = {
            "hire_date": row["HIRE DATE"],
            "compensation": row[compensation_key],
        }
        data.append(d)
    return data


