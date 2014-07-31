from datetime import date

from . import base
from . import mixins

from .. import cleaver


class TransformedRecord(base.BaseTransformedRecord, mixins.RaceMixin,
                        mixins.GenericCompensationMixin, mixins.LinkMixin):
    MAP = {
        'compensation': 'ANNUAL SALARY (HOURLY RATE FOR PT)',
        'hire_date': 'CURRENT HIRE DATE',
        'first_name': 'FIRST NAME',
        'last_name': 'LAST NAME',
        'race': 'RACE/ETHNICITY',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    DATE_PROVIDED = date(2013, 8, 31)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/collin_college/salaries/2013-07/collin_college.xlsx'

    def __init__(self, data):
        super(TransformedRecord, self).__init__(data)
        self.process_compenstation_type_and_job_title()

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
            'identifier': base.create_hash_for_record(self.data,
                    exclude=[self.compensation_key, ]),
        }

    @property
    def person(self):
        name = self.get_name()
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
            'classification': 'Community College'
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
                            'tenure': self.calculate_tenure()
                        },
                        'tx_salaries.EmployeeTitle': {
                            'name': self.job_title,
                        },
                    },
                    {
                        'tx_salaries.CompensationType': {
                            'name': 'Associate Professor per Lab Hour',
                        },
                        'tx_salaries.Employee': {
                            'hire_date': hire_date,
                            'compensation': '575',
                            'tenure': self.calculate_tenure()
                        },
                        'tx_salaries.EmployeeTitle': {
                            'name': self.job_title,
                        },
                    }
                ]
            elif self.is_valid:
                # This is someone whose salary we can't even really
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
                        'tenure': self.calculate_tenure()
                    },
                    'tx_salaries.EmployeeTitle': {
                        'name': self.job_title,
                    },
                },
            ]


transform = base.transform_factory(TransformedRecord)
