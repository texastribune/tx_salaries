from copy import copy

from . import base
from .. import cleaver


def transform(labels, source):
    data = []
    for raw_row in source:
        row = dict(zip(labels, raw_row))
        d = copy(base.DEFAULT_DATA_TEMPLATE)

        compensation_key = 'ANNUAL SALARY (HOURLY RATE FOR PT)'

        job_title = row["JOB TITLE"].strip()
        compensation_type = "Full Time"
        if job_title[-2:].upper() == "PT":
            compensation_type = "Part Time"
            job_title = job_title[:-2].strip()

        job_title = job_title.title()

        # Clean up any issues with the "- PT" suffix, but do it by
        # splitting on "-" to ensure that we catch as many as possible
        #
        # TODO: Fix this so its actually correct
        if '-' in row['DEPARTMENT']:
            split_department = row['DEPARTMENT'].split('-')[:-1]
        else:
            split_department = [row['DEPARTMENT'], ]
        raw_department = '-'.join([a.strip() for a in split_department]).title()
        department = cleaver.DepartmentNameCleaver(raw_department).parse()

        raw_name = "%s %s" % (row["FIRST NAME"], row["LAST NAME"])
        name = cleaver.EmployeeNameCleaver(raw_name).parse()

        d["original"] = raw_row
        d['tx_people.Identifier'] = {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_row(row,
                    exclude=[compensation_key, ])
        }

        d["tx_people.Person"] = {
            "family_name": name.last,
            "given_name": name.first,
            "additional_name": name.middle,
            "name": unicode(name),
            "gender": row["SEX"],
        }

        d["tx_people.Organization"] = {
            "name": "Collin College",
            "children": [{
                "name": unicode(department),
            }],
        }

        d["tx_people.Post"] = {
            "label": job_title,
        }

        d["tx_people.Membership"] = {
            "start_date": row["CURRENT HIRE DATE"],
        }

        compensation = row[compensation_key]
        hire_date = row['CURRENT HIRE DATE']
        if compensation == 'See "Explanations" tab':
            if row["JOB TITLE"] == "Assoc Professor":
                d['compensations'] = [
                    {
                        'tx_salaries.CompensationType': {
                            'name': 'Associate Professor per Lecture',
                        },
                        'tx_salaries.Employee': {
                            'hire_date': hire_date,
                            'compensation': '719',
                        },
                    },
                    {
                        'tx_salaries.CompensationType': {
                            'name': 'Associate Professor per Lab Hour',
                        },
                        'tx_salaries.Employee': {
                            'hire_date': hire_date,
                            'compensation': '575',
                        }
                    }
                ]
            elif row['JOB TITLE'] == 'Continuing Ed Instructors':
                # This is someone who's salary we can't even really
                # guess at as no rate is provided by Collin College.
                continue
            else:
                raise Exception('Unable to process')

        else:
            d['compensations'] = [
                {
                    'tx_salaries.CompensationType': {
                        'name': compensation_type,
                    },
                    'tx_salaries.Employee': {
                        'hire_date': hire_date,
                        'compensation': compensation,
                    },
                },
            ]
        data.append(d)
    return data
