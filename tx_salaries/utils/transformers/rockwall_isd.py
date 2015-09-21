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
        # 'middle_name': '', if needed
        # 'full_name': '', if needed
        # 'suffix': '', if needed
        'department': 'Dept',
        'job_title': 'Title',
        'second_title': 'Title2',
        'hire_date': 'Hire Date',
        'compensation': 'Position Contract Amt',
        'gender': 'Gender',
        'race': 'Race Desc',
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
    DATE_PROVIDED = date(2015, 5, 20)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'rockwall_isd/salaries/2015-05/'
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
    def job_title(self):
        raw_title = self.get_mapped_value('job_title')
        second_title = self.get_mapped_value('second_title')
        return ' '.join([raw_title, second_title])


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
