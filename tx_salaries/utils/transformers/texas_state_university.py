from . import base
from . import mixins

from datetime import date
from .. import cleaver

# --row=4


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last name',
        'first_name': 'First name',
        'middle_name': 'Middle name',
        # 'suffix': '', if needed
        'department': 'Organizational Unit',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annual',
        'employee_status': 'Personnel subarea',
        'gender': 'Gender',
        'race': 'Ethnicity',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    # so double check it!
    ORGANIZATION_NAME = 'Texas State University'

    # What type of organization is this?
    # This MUST match what we use on the site,
    # double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 2, 2)

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'texas_state_university/2017-02/texas-state.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

    # This is how the loader checks for valid people.
    # Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.employee_status.strip()

        if 'PT' in employee_type:
            return 'PT'
        elif 'FT' in employee_type:
            return 'FT'

    @property
    def description(self):
        employee_type = self.employee_status.strip()

        if 'PT' in employee_type:
            return "Part-time annual pay"
        elif 'FT' in employee_type:
            return "Annual pay"

    @property
    def person(self):
        name = self.get_name()

        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.get_mapped_value('gender')]
        }

        return r


transform = base.transform_factory(TransformedRecord)
