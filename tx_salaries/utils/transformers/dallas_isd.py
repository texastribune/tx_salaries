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
        'department': 'Organization/Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'Salary',
        'gender': 'Gender',
        'race': 'Ethnicity',
        'status': 'Employee Type',
        'hours': 'Hours Worked',
    }

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Dallas ISD'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2015, 11, 10)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas_isd/salaries/2015-11/dallas_isd.xlsx')

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.job_title.strip() != 'STADIUM WORKER'

    # @property
    # def hire_date(self):
    #     raw_date = self.get_mapped_value('hire_date')
    #     return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

    @property
    def compensation_type(self):
        emp_type = self.status

        if emp_type == 'Full-Time':
            return 'FT'

        if emp_type == 'Part-Time':
            return 'PT'

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender
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
