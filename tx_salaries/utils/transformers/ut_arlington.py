from datetime import date

from . import base
from . import mixins

from .. import cleaver
from decimal import Decimal

# http://raw.texastribune.org.s3.amazonaws.com/ut_arlington/salaries/2014-02/UT%20Arlington%20Salaries.xlsx


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department Title',
        'job_title': 'Job Title',
        'race': 'Ethnic Group',
        'gender': 'Gender',
        'hire_date': 'First Hire Date',
        'compensation': 'Annual Rate',
        'percent_of_fulltime': 'FTE',
        'description': 'Employee Pay Type'
    }

    NAME_FIELDS = ('first_name', 'last_name',)

    gender_map = {'F': 'F', 'M': 'M'}

    ORGANIZATION_NAME = 'University of Texas at Arlington'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given on spreadsheet, but they appear to give part time. 14 people earn < 4000
    @property
    def compensation_type(self):
        if Decimal(self.percent_of_fulltime) < 1:
            return 'PT'
        return 'FT'

    description = 'Annual compensation'

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_arlington/salaries/2015-10/data.xlsx'

    DATE_PROVIDED = date(2015, 10, 27)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != '' and self.hire_date.strip() != ''

transform = base.transform_factory(TransformedRecord)
