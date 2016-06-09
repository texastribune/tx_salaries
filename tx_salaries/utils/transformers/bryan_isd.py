from . import base
from . import mixins

from datetime import date
from .. import cleaver


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department Title',
        'job_title': 'Assignment Title',
        'employee_type': 'Full / Part Time',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Salary',
        #'gender': 'Sex',
        'white': 'White',
        'black': 'Black or African American',
        'asian': 'Asian',
        'native': 'American Indian or Alaskan Native',
        'hawaiian': 'Hawaiian / Pacific Islander',
        'hispanic': 'Of Hispanic or Latino Descent',
        'employee_type': 'Full Time/Part Time',
    }

    race_map = {
         'A': 'Asian',
         'B': 'Black',
         'I': 'American Indian/Alaskan',
         'W': 'White'
    }

    hispanic_map = {'N': 'Non-Hispanic', 'H': 'Hispanic'}

    ORGANIZATION_NAME = 'College Station ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2016, 5, 9)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'college_station_isd/salaries/2016-05/collegestation-isd.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def post(self):
        if self.job_title != '':
            title = self.job_title
        else:
            if self.job_type != '':
                title = self.job_type
            else:
                title = self.secondary_job_type.title()

        return {
            'label': title,
        }

    @property
    def compensations(self):
        if self.job_title != '':
            title = self.job_title
        else:
            if self.job_type != '':
                title = self.job_type
            else:
                title = self.secondary_job_type.title()

        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                    'description': self.description
                },
                'tx_salaries.EmployeeTitle': {
                    'name': title,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                    'tenure': self.calculate_tenure()
                },
            }
        ]

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        return employee_type

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'FT':
            return "Annual Salary"

        if employee_type == 'PT':
            return "Part-time annual salary"

        return "Annual Salary"

    @property
    def race(self):
        given_race = self.race_map[self.given_race.strip()]
        ethnicity = self.hispanic_map[self.hispanic.strip()]

        if given_race == '':
            given_race = 'Not given'
        return {
            'name': given_race + ', ' + ethnicity
        }

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()


transform = base.transform_factory(TransformedRecord)
