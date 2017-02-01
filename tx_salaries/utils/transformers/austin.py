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
        'first_name': 'First',
        'middle_name': 'MI',
        'department': 'Department Name',
        'job_title': 'Title',
        'hire_date': 'Date of Employment',
        'compensation': 'Annual Salary',
        'gender': 'Gender',
        'race': 'Race',
        'employment_type': 'Status'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Austin'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'City'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 1, 27)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'austin/salaries/2017-01/'
           'cityofaustin.xlsx')

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

    @property
    def compensation_type(self):
        status = self.get_mapped_value('employment_type')

        if status == 'Full Time':
            return 'FT'
        elif status == 'Part Time':
            return 'PT'

    @property
    def description(self):
        status = self.get_mapped_value('employment_type')

        if status == 'Full Time':
            return 'Annual salary'
        elif status == 'Part Time':
            return 'Part-time annual salary'

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def race(self):
        given_race = self.get_mapped_value('race')
        if given_race == '':
            given_race = 'Unknown/Not Specified'
        return {'name': given_race}

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

transform = base.transform_factory(TransformedRecord)
