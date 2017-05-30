from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericIdentifierMixin,
    mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Employee Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Latest Hire Date',
        'compensation': 'Annual Salary',
        'gender': 'Gender',
        'race': 'Race',
        'compensation_type': 'Employment Percent*'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Houston ISD'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # Y/M/D agency provided the data
    DATE_PROVIDED = date(2017, 3, 1)

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

    # The URL to find the raw data in our S3 bucket.
    URL = ( 'http://raw.texastribune.org.s3.amazonaws.com/'
            'houston_isd/2017-03/'
            'TPIA.xlsx' )

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
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    @property
    def compensation_type(self):
        comp = float( self.get_mapped_value('compensation') )

        if comp > 55.91:
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        comp = float( self.get_mapped_value('compensation') )

        if comp > 55.91:
            return 'Annual salary'
        else:
            return 'Hourly wage'

transform = base.transform_factory(TransformedRecord)
=======
import re
from datetime import date

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'name': 'Name',
        'department': 'DeptName',
        'job_title': 'Title',
        'compensation_type': 'Full-Time Part-Time',
        'hire_date': 'Last Hire Date',
        'compensation': 'Annual Salary /Hourly Rate',
        'gender': 'Gender',
        'race': 'Category',
    }

    NAME_FIELDS = ('name')

    ORGANIZATION_NAME = 'Houston ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2015, 10, 6)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/houston_isd/houston-2015-10-06.xlsx'

    @property
    def race(self):  # make race capitalization consistent
        return self.get_mapped_value('race').title()

    @property
    def description(self):
        return 'N/A'
        
transform = base.transform_factory(TransformedRecord)