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
        'full_name': 'Full Name Last-First-Middle',
        'department': 'Department Title',
        'job_title': 'Job Type',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Salary',
        'gender': 'Sex',
        'race': 'Race',
        'ethnicity': 'Hispanic',
        'employee_type': 'Full Time/Part Time',
    }

    race_map = {
         'A': 'Asian',
         'B': 'Black',
         'I': 'American Indian/Alaskan',
         'W': 'White'
    }

    ethnicity_map = {'N': 'Non-Hispanic', 'H': 'Hispanic'}

    ORGANIZATION_NAME = 'College Station ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2016, 4, 29)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'college_station_isd/salaries/2016-04/collegestationISD.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def hire_date(self):
        raw_date = self.get_mapped_value('hire_date')
        return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

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
        race = self.get_mapped_value('race').strip()
        hispanic = self.get_mapped_value('ethnicity').strip()

        if race == '':
            race = 'Not given'
        return {
            'name': race + ', ' + hispanic
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
