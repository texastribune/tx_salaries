from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'full_name': 'Employee Full Name',
        'department': 'Organization Name',
        'job_title': 'Job Name',
        'gender': 'Gender',
        'race': 'Ethnic Origin',
        'hire_date': 'Date Of Hire',
        'compensation': 'Actual Annual Salary'
    }

    ORGANIZATION_NAME = 'The University of Texas-Pan American'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given on spreadsheet
    compensation_type = 'Full Time'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    def process_name(self, name):
        # TODO parse middle names
        comma_split = name.split(',')
        space_split = comma_split[1].strip().split(' ')
        given_name = u' '.join(space_split[1:])
        return {
            'given_name': given_name.strip(),
            'family_name': comma_split[0].strip()
        }

    @property
    def person(self):
        names = self.process_name(self.full_name)
        data = {
            'family_name': names['family_name'],
            'given_name': names['given_name'],
            'name': " ".join([names['given_name'], names['family_name']]),
            'gender': self.gender,
        }
        return data

    def process_job_title(self, job_title):
        return job_title.split('.')[1]

    @property
    def compensations(self):
        job_title = self.process_job_title(self.job_title)
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': job_title,
                },
            }
        ]


transform = base.transform_factory(TransformedRecord)
