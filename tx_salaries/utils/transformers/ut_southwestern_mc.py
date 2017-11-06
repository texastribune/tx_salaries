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
        'full_name': 'EMPL_NAME',
        'department': 'DEPT_NAME',
        'job_title': 'JOB_TITLE',
        'hire_date': 'LAST_HIRE_DATE',
        'compensation': 'ANNUAL_RATE',
        'gender': 'GENDER',
        'given_race': 'RACE',
        'status': 'FULL-TIME/PART-TIME'
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
    DATE_PROVIDED = date(2017, 5, 26)

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M', 'Unknown': 'F'}

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
        'ut_southwestern_medical/salaries/2017-05/12295_PIR_UTSW_Employees.xlsx')

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
        return {
            'name': self.get_mapped_value('given_race').strip().title()
        }

    @property
    def description(self):
        if self.status == 'PRN':
            return "Annual compensation (on-call employee)"
        elif self.status == 'Full-Time':
            return "Annual compensation"
        else:
            return "Part-time annual compensation"


transform = base.transform_factory(TransformedRecord)
