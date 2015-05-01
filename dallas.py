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
        #'last_name': 'Last',
        #'first_name': 'First',
        #'middle_name': 'MI',
        'full_name': 'Name - Full'
        # 'suffix': '', if needed
        'department': 'Process Level (Departmet)',
        'job_title': 'Job Code Description',
        'hire_date': 'Adjusted Hire Date',
        'compensation': ' Rate of Pay ',
        'hours': 'Annual Hours',
        'gender': 'Gender',
        'race': 'Ethnicity',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    #NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Dallas'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'City'

    # ???
    #compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    #description = 'Rate of Pay'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 4, 29)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas/salaries/2015-04/'
           'cityofdallas0415.xls')

    # How do they track gender? We need to map what they use to `F` and `M`.
    #gender_map = {'Female': 'F', 'Male': 'M'}

    @property
    def compensation_type(self):
        if self.get_mapped_value('hours') < 2000:
            return 'PT'
        return 'FT'

    @property
    def description(self):
        hours = self.get_mapped_value('hours')

        if not hours:
            return "Full-time salary"

        if hours < 2000:
            return "Part-time salary"

        return "Full-time salary"

    @property
    def compensation(self):
        if self.get_mapped_value('compensation') < 1000:
            return self.get_mapped_value('compensation') * self.get_mapped_value('hours')
        return self.get_mapped_value('compensation')

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

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

    def get_raw_name(self):
        split_name = self.full_name.split(', ')
        last_name = split_name[0]
        split_firstname = split_name[1].split(' ')
        first_name = split_firstname[0]
        if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
            middle_name = split_firstname[1]
        else:
            first_name = split_name[1]
            middle_name = ''

        return u' '.join([first_name, middle_name, last_name])

transform = base.transform_factory(TransformedRecord)
