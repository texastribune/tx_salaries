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
        'department': 'Department Title',
        'job_title': 'Contract Title',
        'hire_date': 'Hire Date',
        'compensation': 'Salary/Hourly or Daily Rate',
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
    DATE_PROVIDED = date(2017, 5, 9)

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'cypress_fairbanks_isd/salaries/2017-05/cypress-fairbanks-isd.xlsx')

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
        status = self.get_mapped_value('employee_type').strip()
        jobTitle = self.get_mapped_value('department').strip()
        salary = float(self.get_mapped_value('compensation'))
        # If the employee isn't a sub, their rate is more than $100 and
        # they're a full-time employee, their pay is their Annual salary
        if jobTitle != 'SUBSTITUTE' and salary > 100.00 and status == 'F':
            return 'Annual salary'
        # If the employee isn't a sub, their salary is more than $100, and
        # then their pay is their Part-time salary
        elif jobTitle != 'SUBSTITUTE' and salary > 100.00:
            return 'Part-time salary'
        # If the employee isn't a sub and their salary is less than $100,
        # then their pay is an hourly rate
        elif jobTitle != 'SUBSTITUTE' and salary < 100.00:
            return 'Hourly rate'
        # If the employee is a sub, their salary is a daily rate
        elif jobTitle == 'SUBSTITUTE':
            return 'Daily rate'

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    @property
    def compensation_type(self):
        status = self.get_mapped_value('employee_type').strip()
        jobTitle = self.get_mapped_value('department').strip()
        salary = float(self.get_mapped_value('compensation'))
        # If the employee isn't a sub, their rate is more than $100 and
        # they're a full-time employee, their pay is their Annual salary
        if jobTitle != 'SUBSTITUTE' and salary > 100.00 and status == 'F':
            return 'FT'
        # If the employee isn't a sub, their salary is more than $100, and
        # then their pay is their Part-time salary
        elif jobTitle != 'SUBSTITUTE' and salary > 100.00:
            return 'PT'
        # If the employee isn't a sub and their salary is less than $100,
        # then their pay is an hourly rate
        elif jobTitle != 'SUBSTITUTE' and salary < 100.00:
            return 'PT'
        # If the employee is a sub, their salary is a daily rate
        elif jobTitle == 'SUBSTITUTE':
            return 'PT'

    @property
    def job_title(self):
        jobTitle = self.get_mapped_value('job_title').strip().upper()
        departmentName = self.get_mapped_value('department').strip().upper()
        substitute = 'Substitute'
        if departmentName == 'SUBSTITUTE' and jobTitle == '':
            return substitute
        else:
            return jobTitle

    @property
    def department(self):
        jobDepartment = self.get_mapped_value('department').strip().upper()
        return jobDepartment

    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            tenure = 0
        return tenure

transform = base.transform_factory(TransformedRecord)
