from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Rehire Dt',
        'gender': 'Sex',
        'race': 'Ethnic Grp',
        'compensation': 'Comp Rate',
        'compensation_type': 'Full/Part',
        'pay_type': 'Hourly/Salary'
    }

    # The order of the name fields to build a full name.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'The University of Texas Health Science Center at San Antonio'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2019, 8, 14)

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
    'ut_health_san_antonio/salaries/2019-09/454_Essig_TPIA_responsive_doc.xls')

    gender_map = {
        'Female':'F',
        'Male':'M',
        'Unknown': 'Unknown'
    }

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
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    @property
    def compensation(self):
        comp = self.get_mapped_value('compensation')

        if comp == '':
            comp = '0'

        return comp

    @property
    def compensation_type(self):
        comp_type = self.get_mapped_value('compensation_type')

        if comp_type == 'Full-Time':
            return 'FT'
        else:
            return 'PT'
        return ''

    @property
    def description(self):
        comp_type = self.get_mapped_value('compensation_type')
        pay_type = self.get_mapped_value('pay_type')

        if pay_type == 'S' and comp_type == 'Full-Time':
            return 'Annual salary'
        elif pay_type == 'S' and comp_type == 'Part-Time':
            return 'Part time annual salary'
        elif pay_type == 'H' and comp_type == 'Full-Time':
            return 'Full time hourly wage'
        elif pay_type == 'H' and comp_type == 'Part-Time':
            return 'Part time hourly wage'

    @property
    def race(self):
        race = self.get_mapped_value('race')

        if race == '':
            race = 'Unknown'

        return {'name': race}

    @property
    def department(self):
        dept = self.get_mapped_value('department')

        return dept

    def get_raw_name(self):
        split_name = self.full_name.split(',')
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
