from . import base
from . import mixins

from datetime import date
from decimal import Decimal

class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name - Full',
        'department': 'Process Level (Departmet)',
        'job_title': 'Job Code Description',
        'hire_date': 'Adjusted Hire Date',
        'compensation': 'Rate of Pay',
        'hours': 'Annual Hours',
        'gender': 'Gender',
        'nationality': 'Ethnicity',
    }

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Dallas'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'City'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 4, 29)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas/salaries/2015-04/'
           'cityofdallas0415.xls')

    race_map = {
        'AMIN': 'American Indian',
        'ASIN': 'Asian Indian',
        'BLK': 'Black',
        'CHIN': 'Chinese',
        'CUBA': 'Cuban',
        'FILI': 'Filipino',
        'GUAM': 'Guamanian',
        'HAWA': 'Native Hawaiian',
        'JAPN': 'Japanese',
        'KORN': 'Korean',
        'MEXA': 'Mexican, Mexican Amer, Chicano',
        'OASI': 'Other Asian',
        'OTHR': 'Some Other Race',
        'PACF': 'Other Pacific Islander',
        'PUER': 'Puerto Rican',
        'SAMO': 'Samoan',
        'SPAN': 'Other Spanish/Hispanic/Latino',
        'TWO': 'Two or More Races',
        'VIET': 'Vietnamese',
        'WHT': 'White',
    }

    @property
    def compensation_type(self):
        hours = self.hours

        if not hours:
            return 'FT'

        if int(hours) < 2000:
            return 'PT'

        return 'FT'

    @property
    def description(self):
        hours = self.hours

        if not hours:
            return "Full-time salary"

        if int(hours) < 2000:
            return "Part-time salary"

        return "Full-time salary"

    @property
    def compensation(self):
        comp = Decimal(self.get_mapped_value('compensation'))

        if comp < 1000:
            return comp * int(self.hours)
        return self.get_mapped_value('compensation')

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def race(self):
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
        split_name = self.full_name.split(', ')
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
