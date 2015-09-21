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
        'last_name': 'LAST',
        'first_name': 'FIRST',
        # 'middle_name': '', if needed
        # 'full_name': '', if needed
        # 'suffix': '', if needed
        'department': 'DEPARTMENT',
        'job_title': 'POSITION',
        'hire_date': 'HIREDATE',
        'compensation': 'SALARY',
        'gender': 'SEX',
        'nationality': 'ETH',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Austin ISD'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # ???
    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Gross annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 4, 6)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'austin_isd/salaries/2015-04/'
           'austin-isd.xls')

    race_map = {
        'W': 'White',
        'B': 'Black',
        'H': 'Hispanic',
        'A': 'Asian',
        'I': 'Did not respond',
        'P': 'Pacific Islander',
        'S': 'Asian',
        'M': 'Mixed Race',
    }

    # How do they track gender? We need to map what they use to `F` and `M`.
    # gender_map = {'Female': 'F', 'Male': 'M'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            # 'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

    # @property
    # def hire_date(self):
    #     print self.get_mapped_value()
    #     raw_date = self.get_mapped_value('hire_date')
    #     return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

transform = base.transform_factory(TransformedRecord)
