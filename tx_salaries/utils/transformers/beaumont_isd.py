from . import base
from . import mixins
from .. import cleaver
from datetime import date

import string

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'PER_LAST_NAME',
        'first_name': 'PER_FIRST_NAME',
        'middle_name': 'PER_MIDDLE_NAME',
        'department': 'Organization',
        'job_title': 'ROLE_NAME',
        'hire_date': 'EMP_HIRE_DT',
        'compensation': 'EMP_ASGN_PAY_HIST_A_NRML_PAY',
        'hourly_rate': 'Hourly Rate',
        'gender': 'PER_GENDER',
        'race': 'PRIMARY_ETHNICITY_CODE',
        'employee_type': 'Status'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Beaumont ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2018, 5, 7)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'beaumont_isd/salaries/2018-06/foia.xlsx')

    @property
    def is_valid(self):
        return self.employee_type.strip() != 'Contract'

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Full Time':
            return 'FT'

        if employee_type == 'Part Time':
            return 'PT'

        return 'FT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'Full Time':
            return "Budgeted Salary"

        if employee_type == 'Part Time':
            return "Part-time hourly rate"

        return "Budgeted Salary"

    @property
    def compensation(self):
        salary = self.get_mapped_value('compensation')
        wage = self.get_mapped_value('hourly_rate')
        employee_type = self.employee_type

        if employee_type == 'Part Time':
            return wage
        else:
            return salary

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
            'gender': self.gender,
        }

        return r

transform = base.transform_factory(TransformedRecord)
