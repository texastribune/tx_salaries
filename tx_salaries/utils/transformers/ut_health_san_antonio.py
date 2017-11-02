from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericIdentifierMixin,
    mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'Gross Annual Salary',
        'gender': 'Gender',
        'race': 'Race',
        'compensation_type': 'Full/Part'
    }

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'The University of Texas Health Science Center at San Antonio'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 7, 3)

    # The URL to find the raw data in our S3 bucket.
    URL = 'http://raw.texastribune.org.s3.amazonaws.com/'
    'ut_health_san_antonio/salaries/2017-11/Texas_Tribune_Data_6-30-17.xlsx'

    @property
    def is_valid(self):
        comp_type = self.get_mapped_value('compensation_type')

        # check for name length is because CSVKit keeps going on an empty row for some reason
        return comp_type != 'Non-regular' and len(self.full_name) != 0

        # Adjust to return False on invalid fields.  For example:
        # return self.full_name.strip() != ''

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

    @property
    def compensation(self):
        comp = self.get_mapped_value('compensation')

        if comp == 'Varies':
            return 0
        else:
            return comp

    @property
    def compensation_type(self):
        comp_type = self.get_mapped_value('compensation_type')

        if comp_type == 'Full Time' or comp_type == 'DUAL':
            return 'FT'
        else:
            return 'PT'
        return ''

    @property
    def description(self):
        comp = self.get_mapped_value('compensation')
        comp_type = self.get_mapped_value('compensation_type')

        if comp == 'Varies':
            return "Pay varies"
        elif comp_type == 'DUAL':
            return 'Annual gross salary (DUAL employment)'
        elif comp_type == 'Part Time':
            return 'Annual gross salary (Part time)'
        else:
            return 'Annual gross salary'

    # Alain = Ah-Lane

transform = base.transform_factory(TransformedRecord)
