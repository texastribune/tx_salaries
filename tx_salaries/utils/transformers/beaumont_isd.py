from . import base
from . import mixins

from datetime import date


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
        'gender': 'PER_GENDER',
        'race': 'PRIMARY_ETHNICITY_CODE',
        'employee_type': 'Status'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Beaumont ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2018, 6, 14)

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/beaumont/'
           'salaries/beaumont/foia.xlsx')

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Part-Time':
            return 'PT'

        if employee_type == '':
            return 'FT'

        return 'FT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == '':
            return "Yearly salary"

        if employee_type == 'Part-Time':
            return "Part-time, hourly rate"

        return "Yearly salary"

    # @property
    # def compensation(self):
    #     salary = self.get_mapped_value('compensation')
    #     wage = self.get_mapped_value('hourly_rate')
    #     employee_type = self.employee_type

    #     if employee_type == 'Part-Time':
    #         return wage
    #     else:
    #         return salary

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender,
        }

        return r

transform = base.transform_factory(TransformedRecord)
