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
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Gross',
        'gender': 'Gender',
        'race': 'Race',
        'compensation_type': 'FT/PT'
    }
    
    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Hays County'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'County'

    # Y/M/D agency provided the data
    DATE_PROVIDED = date(2017, 03, 01)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'hays_county/salaries/2017-03/'
           'raw.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''
 
    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

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
    def compensation_type(self):
        emptype = self.get_mapped_value('compensation_type')

        return emptype

    @property
    def description(self):
        emptype = self.get_mapped_value('compensation_type')

        if emptype == 'FT':
            return 'Annual gross salary'
        elif emptype == 'PT':
            return 'Part-time, annual gross salary'

    @property
    def department(self):
        dept = self.get_mapped_value('department')

        if dept == 'Transportation/Transportation':
            return 'Transportation'
        else:
            return dept

transform = base.transform_factory(TransformedRecord)