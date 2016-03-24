from . import base
from . import mixins

from datetime import date


# http://raw.texastribune.org.s3.amazonaws.com/ut_dallas/salaries/2014-02/FOIA%20Request%20-%20Tribune.xlsx

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'full_name': 'Name',
        'department': 'Dept Desc',
        'job_title': ' Pos Title',
        'hire_date': 'Hire date',
        'nationality': 'Ethnicity/Race',
        'gender': 'Gender',
        'compensation': 'FY 2015 Gross Pay',
    }

    ORGANIZATION_NAME = 'Austin Community College'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
          'ut_dallas/salaries/2015-05/ut_dallas.xls')

    race_map = {
         'NHS': 'Non-Hispanic/Latino',
         'WH': 'White',
         'AN': 'American/Alaska Native',
         'AS': 'Asian',
         'BL': 'Black or African American',
         'HP': 'Hawaiian/Pacific Islander',
         'HIS': 'Hispanic'
    }

    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual Rate'

    DATE_PROVIDED = date(2015, 5, 27)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation(self):
        raw = self.get_mapped_value('compensation')
        return raw.strip(' $').replace(',', '')

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
