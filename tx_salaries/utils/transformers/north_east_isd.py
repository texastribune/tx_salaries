from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Location',
        'job_title': 'Job Name',
        'hire_date': 'Hire Date',
        'compensation': 'Base Salary',
        'gender': 'Sex',
        'race': 'Race',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'North East ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2014, 6, 30)
    # Y/M/D agency provided the data

    URL = "http://raw.texastribune.org.s3.amazonaws.com/north_east_isd/salaries/2014-06/TPIA%20Response%20%20-%20Texas%20Tribune%20June%202014.xlsx"

    compensation_type = 'FT'
    description = 'Base Salary'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    # department names have three digits and a whitespace in front
    def department_as_child(self):
        return [{'name': self.department[4:], }, ]

transform = base.transform_factory(TransformedRecord)
