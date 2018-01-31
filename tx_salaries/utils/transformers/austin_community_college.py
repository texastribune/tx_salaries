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
        'full_name': 'Ppwg Name',
        'department': 'A Ppwg Dept Desc',
        'job_title': 'A Ppwg Pos Title',
        'hire_date': 'Employment Date',
        'nationality': 'Race',
        'ethnicity': 'Ethnicity',
        'gender': 'Gender',
        'FTPT': 'PT/FT',
        'compensation': 'Calendar Year 2017 Salary',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'Austin Community College'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'Community College'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2018, 1, 31)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'austin_community_college/salaries/2018-01/ORR_1752_BU_snt_1-24-18.xlsx')

    # How would you describe the compensation field? We try to respect how
    # they use their system.
    description = 'Gross Pay'

    race_map = {
        'NHS': 'Non-Hispanic/Latino',
        'WH': 'White',
        'BL': 'Black',
        'HIS': 'Hispanic',
        'AN': 'American/Alaska Native',
        'AS': 'Asian',
        'HP': 'Hawaiian/Pacific Islander',
        'Unknown': 'Unknown'
    }

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

    # This is how the loader checks for valid people. Defaults to checking to
    # see if `full_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('FTPT')

        return emptype

    def print_compensation(self):
        compensation = self.compensation
        print compensation

    @property
    def race(self):
        raw = self.get_mapped_value('nationality')
        races = raw.split(',')
        if len(races) > 1:
            return {
                'name': 'Two or more races'
            }
        return {
            'name': self.race_map[self.nationality.strip()]
        }


    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()

transform = base.transform_factory(TransformedRecord)
