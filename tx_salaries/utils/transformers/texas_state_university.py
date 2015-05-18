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
        # 'last_name': '',
        # 'first_name': '',
        # 'middle_name': '', if needed
        'full_name': 'Name',
        # 'suffix': '', if needed
        'department': 'Organizational Unit',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'ANNUAL Calculation',
        'compensation_key': 'Compensation Key',
        'gender': 'Gender',
        'race': 'Ethnicity',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    # NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    # so double check it!
    ORGANIZATION_NAME = 'Texas State University'

    # What type of organization is this?
    # This MUST match what we use on the site,
    # double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # ???
    compensation_type = 'FT'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 4, 8)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'texas_state_university/2015-04/'
           'Texas_State_University04082015.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

    # This is how the loader checks for valid people.
    # Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

    @property
    def description(self):
        key = self.get_mapped_value('compensation_key')

        if key == 'ANNUAL 9 Month Calculation':
            return 'Annual 9 month calculation'

        if key == 'ANNUAL 12 Month Calculation':
            return 'Annual 12 month calculation'

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

    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()


transform = base.transform_factory(TransformedRecord)
