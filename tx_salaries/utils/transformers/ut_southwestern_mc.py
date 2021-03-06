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

    # REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'full_name': 'Primary Name',
        'department': 'Department Description',
        'job_title': 'Job Code Description',
        'hire_date': 'Date First Hire',
        'compensation': 'Annual Pay',
        'gender': 'Gender',
        'given_race': 'RACE',
        'status': 'Full Time Type Description',

        'race_american_indian': 'Race American Indian Flag',
        'race_asian': 'Race Asian Flag',
        'race_pacific_islander': 'Race Pacific Islander Flag',
        'race_african_american': 'Race African American Flag',
        'race_white': 'Race White Flag'
    }

     # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'UT Southwestern Medical Center'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2019, 7, 30)

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M', 'Unknown': 'Unknown'}

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
        'ut_southwestern_medical/salaries/2019/TPIA_Data_Release.xlsx')

    # This is how the loader checks for valid people. Defaults to checking to
    # see if `full_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields. For example:
        return self.full_name.strip() != ''

    @property
    def compensation_type(self):
        if self.status == 'Full-Time':
            return 'FT'
        else:
            return 'PT'

    @property
    def compensation(self):
        comp = self.get_mapped_value('compensation')

        if not comp:
            return 0
        else:
            return comp

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

        # If we don't have a name that looks like so:
        # Jones,Mike
        # The name isn't parsed into first, last properly
        # So we'll parse it out manually by splitting it by the comma
        # And reversing order so we end up with:
        # Mike Jones
        if ',' in r['name']:
            if ', ' not in r['name']:
                name_split = r['name'].split(',')

                r['name'] = name_split[1] + ' ' + name_split[0]

        return r

    @property
    def job_title(self):
        # don't title case roman numerals
        title = self.get_mapped_value('job_title')
        split = title.split('II')
        split_two = title.split('IV')
        split_three = title.split(' V')

        if len(split) == 1 and len(split_two) == 1  and len(split_three) == 1:
            return title.title()
        elif len(split) > 1:
            return split[0].title() + ' II' + split[1]
        elif len(split_two) > 1:
            return split_two[0].title() + ' IV'
        elif len(split_three) > 1:
            return split_three[0].title() + ' V'

    @property
    def race(self):
        if self.race_american_indian == 'Y':
            race = 'American Indian'
        elif self.race_asian == 'Y':
            race = 'Asian'
        elif self.race_pacific_islander == 'Y':
            race = 'Pacific Islander'
        elif self.race_african_american == 'Y':
            race = 'African American'
        elif self.race_white == 'Y':
            race = 'White'
        else:
            race = 'Unknown'

        return {'name': race}

    @property
    def description(self):
        if self.status == 'PRN':
            return "Annual compensation (on-call employee)"
        elif self.status == 'Full-Time':
            return "Annual compensation"
        else:
            return "Part-time annual compensation"


transform = base.transform_factory(TransformedRecord)
