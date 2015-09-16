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
        'last_name': 'LAST_NAME',
        'first_name': 'FIRST_NAME',
        'department': 'DEPARTMENT',
        'job_title': 'TITLE',
        'hire_date': 'ORIGINAL_DATE_OF_HIRE',
        'compensation': 'ANNUAL_SALARY',
        'gender': 'SEX',
        'nationality': 'ETHNICITY',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Texas Woman\'s University'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # ???
    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 7, 9)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'texas_womans_university/salaries/2015-07/'
           'texas_womans_university.xls')

    race_map = {
        'Asian (Not Hispanic or Latino)': 'Asian (Not Hispanic or Latino)',
        'White (Not Hispanic or Latino)': 'White (Not Hispanic or Latino)',
        'American Indian or Alaskan Native (Not Hispanic or Latino)': 'American Indian or Alaskan Native (Not Hispanic or Latino)',
        'Native Hawiian or Other Pacific (Not Hispanic/Latino)': 'Native Hawiian or Other Pacific (Not Hispanic/Latino)',
        'Black or African American (Not Hispanic or Latino)': 'Black or African American (Not Hispanic or Latino)',
        'HAWAIIAN': 'Native Hawaiian/Other Pacific Islander',
        'UKN': 'Not Known',
        'Hispanic or Latino': 'Hispanic or Latino',
        'Not Known': 'Not Known',
    }

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.first_name.strip() != ''

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
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

transform = base.transform_factory(TransformedRecord)
