from copy import copy

from . import base
from .. import cleaver


class TransformedRow(object):
    def __init__(self, data):
        self.data = data
        self.compensation_key = 'ANNUAL SALARY (HOURLY RATE FOR PT)'

        self.process_compenstation_type_and_job_title()

    @property
    def hire_date(self):
        return self.data['CURRENT HIRE DATE']

    @property
    def compensation(self):
        return self.data[self.compensation_key]

    @property
    def is_valid(self):
        return self.job_title != 'Continuing Ed Instructors'

    @property
    def is_special_case_compensation(self):
        return self.compensation == 'See "Explanations" tab'

    def process_compenstation_type_and_job_title(self):
        self.compensation_type = 'Full Time'
        self.job_title = self.data['JOB TITLE'].strip()
        if self.job_title[-2:].upper() == 'PT':
            self.compensation_type = 'Part Time'
            self.job_title = self.job_title[:-2].strip()

        self.job_title = self.job_title.title()

    @property
    def raw_name(self):
        return '%s %s' % (self.data['FIRST NAME'], self.data['LAST NAME'])

    def name(self):
        return cleaver.EmployeeNameCleaver(self.raw_name).parse()

    def department(self):
        # Clean up any issues with the '- PT' suffix, but do it by
        # splitting on '-' to ensure that we catch as many as possible
        #
        # TODO: Fix this so its actually correct
        if '-' in self.data['DEPARTMENT']:
            split_department = self.data['DEPARTMENT'].split('-')[:-1]
        else:
            split_department = [self.data['DEPARTMENT'], ]
        raw_department = '-'.join([a.strip() for a in split_department]).title()
        return cleaver.DepartmentNameCleaver(raw_department).parse()

    @property
    def identifier(self):
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_row(self.data,
                    exclude=[self.compensation_key, ])
        }

    @property
    def person(self):
        name = self.name()
        return {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.data['SEX'],
        }

    @property
    def organization(self):
        return {
            'name': 'Collin College',
            'children': [{
                'name': unicode(self.department()),
            }],
        }

    @property
    def post(self):
        return {
            'label': self.job_title,
        }

    @property
    def membership(self):
        return {
            'start_date': self.hire_date,
        }

    @property
    def compensations(self):
        hire_date = self.hire_date
        if self.is_special_case_compensation:
            if self.job_title == 'Assoc Professor':
                return [
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
            elif self.is_valid:
                # This is someone who's salary we can't even really
                # guess at as no rate is provided by Collin College.
                #
                # NOTE: This should no longer be accessed
                return None
            else:
                raise Exception('Unable to process')

        else:
            return [
                {
                    'tx_salaries.CompensationType': {
                        'name': self.compensation_type,
                    },
                    'tx_salaries.Employee': {
                        'hire_date': hire_date,
                        'compensation': self.compensation,
                    },
                },
            ]


def transform_row(row):
    obj = TransformedRow(row)
    # Stop early if this isn't valid
    if not obj.is_valid:
        return

    d = copy(base.DEFAULT_DATA_TEMPLATE)
    d['original'] = row

    d['tx_people.Identifier'] = obj.identifier
    d['tx_people.Person'] = obj.person
    d['tx_people.Organization'] = obj.organization
    d['tx_people.Post'] = obj.post
    d['tx_people.Membership'] = obj.membership
    d['compensations'] = obj.compensations
    return d


def transform(labels, source):
    data = []
    for raw_row in source:
        row = dict(zip(labels, raw_row))
        processed = transform_row(row)
        if processed:
            data.append(processed)
    return data
