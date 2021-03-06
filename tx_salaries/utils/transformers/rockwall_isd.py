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
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department-Campus',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'hispanic_ethnicity': 'Hispanic Ethnicity',
        'compensation': 'Gross annual salary',
        'gender': 'Gender',
        'ethnicity': 'Federal Race',
        'employee_type': 'Full Time/Part Time Status',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Rockwall ISD'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # ???
    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 2, 13)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'rockwall_isd/salaries/2017-02/'
           'rockwall_isd.xls')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.first_name.strip() != ''

    @property
    def hire_date(self):
        raw_date = self.get_mapped_value('hire_date')
        return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

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

    @property
    def race(self):
        fed_race = self.get_mapped_value('ethnicity')
        hispanic_ethnicity = self.get_mapped_value('hispanic_ethnicity')
        if hispanic_ethnicity == 'Y':
            return {'name': 'Hispanic ' + fed_race}
        elif hispanic_ethnicity == 'N':
            return {'name': 'Non-Hispanic ' + fed_race}

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Full Time':
            return 'FT'
        elif employee_type == 'Part Time':
            return 'PT'
        elif employee_type == '00 - Do Not Report':
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'Full Time':
            return 'Gross annual salary'

        if employee_type != 'Full Time':
            return 'Part-time annual salary'


transform = base.transform_factory(TransformedRecord)
