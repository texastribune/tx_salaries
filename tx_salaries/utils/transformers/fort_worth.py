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
        'last_name': 'Last',
        'first_name': 'First Name',
        # 'middle_name': '', if needed
        # 'full_name': '', if needed
        # 'suffix': '', if needed
        'department': 'Department',
        'job_title': 'Job',
        'hire_date': 'Last Start',
        'compensation': 'Annual Rt',
        'gender': 'Sex',
        'nationality': 'Ethnic Grp',
        'employee_type': 'Full/Part Time'
    }

    RACE_MAP = {
        'WHITE': 'White',
        'BLACK': 'Black/African American',
        'HISPA': 'Hispanic/Latino',
        'ASIAN': 'Asian',
        'NSPEC': 'Not specified',
        'PACIF': 'Native Hawaiian/Other Pacific Islander',
        'AMIND': 'American Indian/Alaska Native',
        '2ORMORE': 'Two or more races'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Fort Worth'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'City'

    # # ???
    # compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2016, 11, 30)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'fort_worth/salaries/2016-11/fort_worth.xls')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M', 'U': 'Unknown'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.first_name.strip() != ''

    @property
    def race(self):
        return {
            'name': self.RACE_MAP[self.nationality.strip()]
        }

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Full-Time':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'Full-Time':
            return 'Gross annual salary'

        if employee_type == 'Part-Time':
            return 'Part-time annual salary'

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            # 'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

transform = base.transform_factory(TransformedRecord)
