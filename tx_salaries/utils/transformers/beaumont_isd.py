from . import base
from . import mixins

from datetime import date

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LNAME',
        'first_name': 'FNAME',
        'department': 'DEPT',
        'job_title': 'TITLE',
        'hire_date': 'HIREDATE',
        'compensation': 'BUDGETED_SALARY',
        'hourly_rate': 'Hourly Rate',
        'gender': 'SEX',
        'race': 'Race',
        'employee_type': 'Status'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Beaumont ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2016, 4, 25)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/beaumont_isd/salaries/2016-04/beaumont_isd.xlsx'

    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False
    #One contract employee is listed, salary is just 'contract'

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
