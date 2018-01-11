from . import base
from . import mixins

import string

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    # REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'full_name': 'Name',
        'department': 'Department Desc',
        'job_title': 'Job Tile',
        'hire_date': 'Orig Hire Date',
        'compensation': 'Annual Rt',
        'employee_type': 'Full/Part',
        'gender': 'Gender',
        'nationality': 'Ethnicity',
    }

    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    # so double check it!
    ORGANIZATION_NAME = 'University of Houston'

    # What type of organization is this?
    # This MUST match what we use on the site,
    # double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # How do they track gender? We need to map what they use to `F` and `M`.
    # gender_map = {'F': 'F', 'M': 'M'}

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'university_houston/salaries/2018-01/univerity-of-houston.xls')

    race_map = {
        'AMIND': 'American Indian',
        'ASIAN': 'Asian',
        'BLACK': 'Black',
        'HISPA': 'Hispanic',
        'NSPEC': 'Not Specified',
        'WHITE': 'White',
        'PACIF': 'Pacific Islander',
    }

    DATE_PROVIDED = date(2018, 1, 8)
    # Y/M/D agency provided the data

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

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

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return 'FT'

        if employee_type == 'P':
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return "Annual salary"

        if employee_type == 'P':
            return "Part-time annual salary"

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }


transform = base.transform_factory(TransformedRecord)
