from copy import copy

from .import base
from .. import cleaver


class ElPasoDepartmentName(cleaver.DepartmentName):
    MAP = cleaver.DepartmentName.MAP + (
        (cleaver.regex_i(r'ADM\.$'), 'Administration'),
        (cleaver.regex_i(r'DIST ATTY'), 'District Attorney'),
        (cleaver.regex_i(r'COATTYADM'), 'County Attorney Administration'),
        (cleaver.regex_i(r'COATTY'), 'County Attorney'),
        (cleaver.regex_i(r'\-TAIP'), '- Treatment Alternative to Incarceration Program'),
        (cleaver.regex_i(r'AP COMMUNITY INTERVENTION CTR'), 'Adult Probation Community Intervention Center'),
        (cleaver.regex_i(r'ADULT PROB-GANG INTERVENTION'), 'Adult Probation - Gang Intervention'),
    )


def transform(labels, source):
    data = []
    for raw_row in source:
        if len(raw_row[0].strip()) is 0:
            continue

        row = dict(zip(labels, raw_row))
        d = copy(base.DEFAULT_DATA_TEMPLATE)
        d['original'] = row
        raw_name = '%s %s %s' % (row['FIRST NAME'], row['MIDDLE'],
                row['LAST NAME'])

        d['tx_people.Identifier'] = {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_row(row, exclude=['PAY RATE', ]),
        }
        name = cleaver.EmployeeNameCleaver(raw_name).parse()
        d['tx_people.Person'] = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': str(name),
            'gender': row['SEX'],
        }

        department = cleaver.DepartmentNameCleaver(row['DEPARTMENT'].title(),
                object_class=ElPasoDepartmentName).parse()
        d['tx_people.Organization'] = {
            'name': str(department),
        }

        d['tx_people.Post'] = {
            'label': row['JOB TITLE'].title(),
        }

        d['tx_people.Membership'] = {
            'start_date': row['HIRE DATE'],
        }

        d['tx_salaries.CompensationType'] = {
            'name': '{0} Time'.format('Part' if row['PART FULL'].strip() == 'P'
                    else 'Full'),
        }

        if row['ANNUAL RATE'].strip() == '0':
            compensation_key = 'PAY RATE'
        else:
            compensation_key = 'ANNUAL RATE'
        d['tx_salaries.Employee'] = {
            'hire_date': row['HIRE DATE'],
            'compensation': row[compensation_key],
        }
        data.append(d)
    return data


