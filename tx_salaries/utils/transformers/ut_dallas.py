from . import base
from . import mixins

from datetime import date


# http://raw.texastribune.org.s3.amazonaws.com/ut_dallas/salaries/2014-02/FOIA%20Request%20-%20Tribune.xlsx

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Department Descr',
        'job_title': 'Job Code Descr',
        'hire_date': 'Hire Date',
        'nationality': 'Race',
        'gender': 'Gender',
        'compensation': 'Comp Rate',
        'employee_type': 'Comp Freq',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at Dallas'

    ORGANIZATION_CLASSIFICATION = 'University'

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
          'ut_dallas/salaries/2017-03/ut-dallas-edit.csv')

    race_map = {
        'AMIND': 'American Indian/Alaska Native',
        'ASIAN': 'Asian or Pacific Islander',
        'BLACK': 'Black, Non-Hispanic',
        'CHN': 'Chinese',
        'HISPA': 'Hispanic/Latino',
        'HAWAIIAN': 'Native Hawaiian/Oth Pacific Islander',
        'KOR': 'Korean',
        'OASN': 'Other Asian',
        'NSPEC': 'Not Specified',
        'WHITE': 'White',
        'VIET': 'Vietnamese',
        'PR': 'Puerto Rican',
        '#N/A': 'Unknown',
    }

    DATE_PROVIDED = date(2017, 3, 15)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        status = self.get_mapped_value('employee_type')

        # hourly rates, everyone else is paid as annual rate
        if status == 'H':
            return 'PT'

        else:
            return 'FT'

    @property
    def description(self):
        status = self.get_mapped_value('employee_type')
        if status == 'A' or status == 'M':
            return "Annual salary"

        if status == 'M9':
            return "Nine-month salary"

        if status == 'H':
            return 'Hourly rate'

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }


transform = base.transform_factory(TransformedRecord)
