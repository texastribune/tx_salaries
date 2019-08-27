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
        'race': 'Ethnicity',
        'employment_type': 'Part Time/Full Time'
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
    DATE_PROVIDED = date(2018, 3, 7)

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/austin/'
           'salaries/2018-03/austin.xls')

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
    # according to City of Austin HR:
    #  We recently had all employees take a look at their ethnicity
    #  identification in our HR System to realign themselves with the approved
    #  ethnicity types by the Department of Labor.  Some employees failed to
    #  make the necessary changes to their ethnicity which are no longer valid
    #  options (i.e., Other, Asian/Pacific Isl).  Because of this, we tied an
    #  Invalid identifier to their ethnicity choice until they can go and
    #  make the necessary changes to their ethnicity choice.
        given_race = self.get_mapped_value('race')
        if given_race == '':
            given_race = 'Unknown/Not Specified'
        elif given_race == '(Invalid) Asian/Pacific Isl':
            given_race = 'Asian/Pacific Islander'
        elif given_race == '(Invalid) Other':
            given_race = 'Other'
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
