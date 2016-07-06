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
        'full_name': 'Employee Name',
        'department': 'Department',
        'job_title': 'Position Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Salary',
        'gender': 'Gender',
        'race': 'Ethnicity',
        'employee_type': 'Fulltime/Part-Time',
    }

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Bexar County'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'County'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2016, 6, 8)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/bexar_county/salaries/2015-06/ORR%20460%20response.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Fulltime':
            return 'FT'

        if employee_type == 'Part-Time':
            return 'PT'

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
