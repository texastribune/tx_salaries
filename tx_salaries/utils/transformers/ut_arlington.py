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
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Rt',
        'gender': 'Gender',
        'nationality': 'Ethnic Group',
        'employee_type': 'Pay Type',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    race_map = {
        'AMIND': 'American Indian',
        'WHITE': 'White',
        'HISPA': 'Hispanic',
        'ASIAN': 'Asian',
        '2+RACE': 'Mixed race',
        'PACIF': 'Pacific Islander',
        'BLACK': 'Black',
        'NSPEC': 'Not specified',
        '': 'Not given',
    }

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'The University of Texas at Arlington'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2016, 6, 30)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/ut_arlington/salaries/2016-06/Release,%20UTA_HR_TX_TRIBUNE_FINAL.xls')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False


    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        return len(self.compensation.strip()) > 1

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Annual Salary':
            return 'Annual Salary'

        if employee_type == '9 Month Salary':
            return '9 Month Salary'

        if employee_type == '12 Month Salary':
            return '12 Month Salary'

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

transform = base.transform_factory(TransformedRecord)
