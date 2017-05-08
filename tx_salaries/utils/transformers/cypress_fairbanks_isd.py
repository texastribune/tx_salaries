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
        'department': 'Department Desc',
        'job_title': 'Contract Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annl Sal',
        'gender': 'Sex',
        'nationality': 'Race',
        'employee_type': 'Part Time',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Cypress-Fairbanks ISD'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # How would you describe the compensation field? We try to respect how they use their system.
    # description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 5, 4)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
        'cypress_fairbanks_isd/salaries/2015-10/203-15.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    race_map = {
        'I': 'American Indian or Alaskan',
        'W': 'White',
        'H': 'Hispanic',
        'A': 'Asian or Pacific Islander',
        'B': 'Black or African American',
        'O': 'Other',
    }

    # This is how the loader checks for valid people.
    # Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.compensation.strip() != '-' and self.last_name.strip() != ''

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

    @property
    def description(self):
        status = self.get_mapped_value('employee_type')

        if status == 'F':
            return 'Annual salary'
        elif status == 'P':
            return 'Part-time salary'

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    @property
    def compensation_type(self):
        employee_type = self.get_mapped_value('employee_type')

        if employee_type == 'F':
            return 'FT'

        if employee_type == 'P':
            return 'PT'

    @property
    def job_title(self):
        jobTitle = self.get_mapped_value('job_title').strip()
        departmentName = self.get_mapped_value('department').strip()
        substitute = 'Substitute'
        if jobTitle and departmentName == 'SUBSTITUTE':
            return jobTitle
        else:
            return substitute

    # def calculate_tenure(self):
    #     hire_date_data = map(int, self.hire_date.split('/'))
    #     print self.get_mapped_value('hire_date')
    #     hire_date = date(hire_date_data[2], hire_date_data[0],
    #                      hire_date_data[1])
    #     tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
    #     if tenure < 0:
    #         return 0
    #     return tenure

transform = base.transform_factory(TransformedRecord)
