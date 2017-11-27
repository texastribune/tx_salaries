from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Last Hire Date',
        'compensation': 'Comp Rate',
        'gender': 'Gender',
        'race': 'Ethnicity',
        'employee_type': 'Overall Status (All Positions)',
        'hourly_salary': 'Hourly/Salary'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'The University of Texas Health Science Center at San Antonio'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 11, 27)

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
    'ut_health_san_antonio/salaries/2017-11/325_-_Essig_TPIA_-_resp_docs.xls')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

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

    @property
    def compensation_type(self):
        emp_type = self.employee_type

        if emp_type == 'Full Time':
            return 'FT'
        else:
            return 'PT'
        return ''

    @property
    def description(self):
        comp_type = self.get_mapped_value('compensation_type')
        emp_type = self.employee_type

        if comp_type == 'Salary' and emp_type == 'Full Time':
            return 'Annual salary'
        elif comp_type == 'Salary' and emp_type == 'Part Time':
            return 'Part time annual salary'
        elif comp_type == 'Hourly' and emp_type == 'Full Time':
            return 'Full time hourly wage'
        elif comp_type == 'Hourly' and emp_type == 'Part Time':
            return 'Part time hourly wage'

transform = base.transform_factory(TransformedRecord)
