from datetime import date

from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
                        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
                        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
                        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    # They included people without compensation and have clarified they do not consider them employees
    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'full_name': 'Name',
        'job_title': 'Job Title',
        'department': 'Dept',
        'race': 'Race',
        'gender': 'Gender',
        'compensation_type': 'Employment Type',
        'hire_date': 'Hire Date',
        'compensation': 'Gross Annual Salary',
        'hourly_comp': 'Hourly Compensation Rate',
    }

    RACE_MAP = {
        'white': 'White',
        'black': 'Black',
        'hispa': 'Hispanic',
        'asian': 'Asian',
        'nspec': 'Not given',
        'pacif': 'Pacific Islander',
        'amind': 'American Indian',
        '': 'Not given'
    }

    gender_map = {'Female': 'F', 'Male': 'M', 'Unknown': 'Not given'}

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
    def race(self):
        return {'name': self.RACE_MAP[self.get_mapped_value('race').strip().lower()]}

    @property
    def compensation(self):
        if self.get_mapped_value('compensation') == 'Varies':
            return self.hourly_comp
        else:
            return self.get_mapped_value('compensation')

    def get_raw_name(self):
        split_name = self.full_name.split(',')
        last_name = split_name[0]
        split_firstname = split_name[1].split(' ')
        first_name = split_firstname[0]
        if len(split_firstname) > 1 and len(split_firstname[1].strip()) > 0:
            middle_name = split_firstname[1]
        else:
            middle_name = ''

        return u' '.join([first_name, middle_name, last_name])



    ORGANIZATION_NAME = 'The University of Texas Health Science Center at Houston'

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # TODO not given on spreadsheet, but they appear to give part time

    @property
    def compensation_type(self):
        if self.get_mapped_value('compensation_type') == 'Full-Time':
            return 'FT'
        elif self.get_mapped_value('compensation_type') == 'Part-Time':
            return 'PT'
        else:
            return ''

    @property
    def description(self):
        if (self.get_mapped_value('compensation_type') == 'Full-Time'
            or self.get_mapped_value('compensation_type') == 'Part-Time'
            or self.get_mapped_value('compensation_type') == 'DUAL'):
            return 'Annual Compensation'
        elif self.get_mapped_value('compensation_type') == 'Hourly':
            return 'Hourly Pay'

    DATE_PROVIDED = date(2015, 10, 8)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_health_houston/salaries/2015-10/uthsca-2015-10-8.xlsx'

    @property
    def is_valid(self):
        # check for name length is because CSVKit keeps going on an empty row for some reason
        return self.get_mapped_value('compensation_type') != 'Non-regular' and len(self.full_name) !=0


transform = base.transform_factory(TransformedRecord)
