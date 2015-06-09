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
        'department': 'Dept Name',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'race': 'Ethnicity',
        'gender': 'Gender',
        'compensation': 'Annual Rt',
    }

    ORGANIZATION_NAME = 'University of Texas at Dallas'

    ORGANIZATION_CLASSIFICATION = 'University'

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
          'ut_dallas/salaries/2015-05/ut_dallas.xls')

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
