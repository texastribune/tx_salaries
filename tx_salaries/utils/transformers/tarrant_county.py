from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Employee Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'compensation': 'Salary',
        'gender': 'Gender',
        'race': 'Ethnicity',
        'employee_type': 'Employment Status',
        'salary_basis': 'Salary Basis',

    }

    ORGANIZATION_NAME = 'Tarrant County'

    ORGANIZATION_CLASSIFICATION = 'County'

    compensation_type = 'FT'

    description = 'Annual rate'

    DATE_PROVIDED = date(2016, 06, 23)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/tarrant_county/salaries/2016-06/2016-06-17%20Texas%20Tribune.xls')

    gender_map = {'Female': 'F', 'Male': 'M'}

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Full-time':
            return 'FT'

        if employee_type == 'Temporary/part-time':
            return 'PT'

    @property
    def description(self):
        if self.salary_basis == 'Annual':
            return 'Annual Compensation'
        elif self.salary_basis == 'Hourly':
            return 'Hourly Pay'

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    def get_raw_name(self):
        split_name = self.full_name.split(', ')

        return u' '.join([split_name[1], split_name[0]])


transform = base.transform_factory(TransformedRecord)
