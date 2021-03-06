from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Dt',
        'compensation': 'Annual Rt',
        'gender': 'Sex',
        'nationality': 'Ethnic Grp',
        'employee_type': 'Full/Part',
    }

    #This organization used to be named 'University of Texas Health Science Center at Tyler'
    #CHECK THE OLD ONE BEFORE PUBLISHING!!!
    ORGANIZATION_NAME = 'UT Health Northeast'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2017, 5, 12)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'ut_health_northeast/2017-05/uthealth-tyler.xls')

    race_map = {
        'AMIND': 'American Indian/Alaska Native',
        'BLACK': 'Black/African American',
        'WHITE': 'White',
        'ASIAN': 'Asian',
        'UNK': 'Ethnicity Unknown',
        'HISPA': 'Hispanic/Latino',
        'PACIF': 'Native Hawaiian/Other Pacific Island'
    }

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        if self.compensation:
            return self.full_name.strip() != ''

    @property
    def compensation_type(self):

        if self.employee_type == 'P':
            return 'PT'
        else:
            return 'FT'

    @property
    def description(self):

        if self.employee_type == 'P':
            return "Part-time annual rate"
        else:
            return "Annual rate"

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
