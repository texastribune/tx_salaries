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
        'department': 'DEPT',
        'job_title': 'TITLE',
        'hire_date': 'ORIGINAL HIRE DATE',
        'compensation': 'ANNUAL SALARY',
        'hourly_rate': 'HOURLY SALARY',
        'gender': 'GENDER',
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
    DATE_PROVIDED = date(2017, 6, 30)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'texas_womans_university/salaries/2015-07/'
           'texas_womans_university.xls')

    # How do they track gender? We need to map what they use to `F` and `M`.
    # gender_map = {'F': 'F', 'M': 'M'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.hire_date.strip() != ''

    @property
    def compensation_type(self):
        annual_salary = self.get_mapped_value('compensation')
        hourly_rate = self.get_mapped_value('hourly_rate')

        if annual_salary:
            return 'FT'

        if hourly_rate:
            return 'PT'

    @property
    def description(self):
        annual_salary = self.get_mapped_value('compensation')
        hourly_rate = self.get_mapped_value('hourly_rate')

        if annual_salary:
            return 'Annual salary'

        if hourly_rate:
            return 'Hourly rate'

    @property
    def compensation(self):
        salary = self.get_mapped_value('compensation')
        wage = self.get_mapped_value('hourly_rate')

        if salary:
            return salary
        else:
            return wage

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            # 'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender
        }

        return r

transform = base.transform_factory(TransformedRecord)
