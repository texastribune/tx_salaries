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
        'last_name': 'LAST NAME',
        'first_name': 'FIRST NAME',
        'department': 'SCHOOL/DEPARTMENT',
        'job_title': 'TITLE',
        'hire_date': 'HIRE DATE',
        'compensation': 'SALARY',
        'employee_type': 'STATUS',
        'gender': 'GENDER',
        'race': 'RACE',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Spring ISD'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # ???
    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 10, 19)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/spring-isd/2015-10/REQUEST%23203.October.7.2015.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M', 'U': 'Unknown'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.first_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.get_mapped_value('employee_type')

        if employee_type == 'FULL':
            return 'FT'

        if employee_type == 'HALF':
            return 'PT'

        return 'FT'

transform = base.transform_factory(TransformedRecord)
