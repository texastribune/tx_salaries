from . import base
from . import mixins

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
