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
        'department': 'Dept Description',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'Salary',
        'employee_type': 'FT/PT',
        'gender': 'Gender',
        'race': 'Race'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Katy ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2018, 6, 14)
    # Y/M/D agency provided the data

    # TODO
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'katy_isd/salaries/2018-06/pir.xlsx')

    description = 'Annual salary'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Full Time':
            return 'FT'

        if employee_type == 'Part Time':
            return 'PT'

    @property
    def hire_date(self):
        raw_date = self.get_mapped_value('hire_date')

        return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

transform = base.transform_factory(TransformedRecord)
