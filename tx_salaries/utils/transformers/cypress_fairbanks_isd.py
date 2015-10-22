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
        'last_name': 'Last Name',
        'first_name': 'First Name',
        # 'middle_name': '', if needed
        # 'full_name': '', if needed
        # 'suffix': '', if needed
        'department': 'Base Location Building Name',
        'job_title': 'Current Job Class Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Salary',
        'gender': 'Sex',
        'nationality': 'Race',
        'employee_type': 'Part Time/Full Time',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Cypress-Fairbanks ISD'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 10, 21)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
        'cypress_fairbanks_isd/salaries/2015-10/203-15.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    race_map = {
        'I': 'Indian',
        'W': 'White',
        'H': 'Hispanic',
        'A': 'Asian',
        'B': 'Black',
        'O': 'Other',
    }

    # This is how the loader checks for valid people.
    # Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.first_name.strip() != ''

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return 'FT'

        if employee_type == 'P':
            return 'PT'

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            # 'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

transform = base.transform_factory(TransformedRecord)
