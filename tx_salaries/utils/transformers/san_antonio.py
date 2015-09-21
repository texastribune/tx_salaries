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
        #'middle_name': 'MI',
        # 'full_name': '', if needed
        # 'suffix': '', if needed
        'department': 'DEPARTMENT',
        'job_title': 'JOB TITLE',
        'hire_date': 'HIRE DATE1',
        'compensation': 'FY14 ANNUAL SALARY2',
        'gender': 'GENDER4',
        'race': 'ETHNIC ORIGIN4',
        'last_day_paid': 'LAST DAY PAID',
        'employee_type': 'EMPLOYEE TYPE',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'San Antonio'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'City'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 5, 28)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'san_antonio/salaries/2015-06/'
           'cityofsanantonio0615.xls')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'FULL TIME':
            return 'FT'

        if employee_type == 'PART TIME':
            return 'PT'

        return 'FT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'FULL TIME':
            return "Annual salary"

        if employee_type == 'PART TIME':
            return "Part-time annual salary"

        return "Annual salary"

    @property
    def compensation(self):
        if self.get_mapped_value('compensation') == '-':
            return 0
        return self.get_mapped_value('compensation')

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.
        if (self.last_day_paid.strip() != '') or (self.employee_type.strip() == 'TEMP'):
            return False
        return True

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

transform = base.transform_factory(TransformedRecord)
