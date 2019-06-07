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
        'department_raw': 'Process Level Desc',
        'job_title': 'Job Code Description',
        'hire_date': 'Hire Date',
        'compensation': 'Rate of Pay',
        'hours': 'Annual Hours',
        'gender': 'Gender',
        'nationality': 'Ethnicity',
        'employment_type': 'Status Description'
    }

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Dallas'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'City'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2019, 5, 1)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas/salaries/2019-04/orr_dallas.xlsx')

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
        status = self.employment_type

        if any(['Full-time' in status, 'Leave' in status]):
            return 'FT'

        if any(['Part-time' in status, 'Intern' in status, 'Seasonal' in status, 'Temporary' in status]):
            return 'PT'

    @property
    def description(self):
        status = self.employment_type

        if any(['Full-time' in status, 'Absence with Pay' in status]):
            return "Full-time annual salary"

        if 'Part-time' in status:
            return "Part-time annual salary"

        if 'Military' in status:
            return 'Full-time annual salary (on non-paid military leave)'

        if 'No Pay' in status:
            return 'Full-time annual salary (on non-paid leave)'

        if any(['Intern' in status, 'Seasonal' in status, 'Temporary' in status]):
            return 'Hourly rate'

    @property
    def compensation(self):
        comp = Decimal(self.get_mapped_value('compensation'))
        status = self.employment_type

        # only want hourly rates for these guys
        if any(['Intern' in status, 'Seasonal' in status, 'Temporary' in status]):
            return comp

        # here we want annual rates, so if they're over $100 its an annual rate
        # if its below we caluclate with annual hours
        if any(['Full-time' in status, 'Leave' in status, 'Part-time' in status]):
            if comp < 101:
                return comp * int(self.hours)
            else:
                return comp

    @property
    def department(self):
        dept = self.department_raw

        return dept.replace("'S", "'s")

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
