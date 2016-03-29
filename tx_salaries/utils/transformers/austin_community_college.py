from . import base
from . import mixins

from .. import cleaver

from datetime import date


class TransformedRecord(
    mixins.GenericCompensationMixin,
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
           'austin_community_college/salaries/2016-02/'
           'austin_community_college.xlsx')

    race_map = {
         'NHS': 'Non-Hispanic/Latino',
         'WH': 'White',
         'AN': 'American/Alaska Native',
         'AS': 'Asian',
         'BL': 'Black or African American',
         'HP': 'Hawaiian/Pacific Islander',
         'HIS': 'Hispanic',
         '2 or more': 'Two or more races',
         'Unknown': 'Unknown'
    }

    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how
    # they use their system.
    description = 'Annual Rate'

    DATE_PROVIDED = date(2016, 2, 26)

    def print_compensation(self):
        compensation = self.compensation
        print compensation


    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

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

    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()

transform = base.transform_factory(TransformedRecord)
