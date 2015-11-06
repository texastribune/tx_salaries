from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin, mixins.GenericDepartmentMixin,
        mixins.GenericIdentifierMixin, mixins.GenericJobTitleMixin,
        mixins.GenericPersonMixin, mixins.MembershipMixin,
        mixins.OrganizationMixin, mixins.PostMixin, mixins.RaceMixin,
        mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LastName',
        'first_name': 'FirstName',
        'middle_name': 'MiddleInitial',
        'department': 'ShortAdlocDesc',
        'job_title': 'ShortTitleDesc',
        'hire_date': 'CurrEmplDate',
        'compensation': 'BudgetedSalary',
        'gender': 'Sex',
        'minority_code': 'EEOMinorityCode',
        'organization_name': 'MbrName',
        'rate': 'AnnualTermMonths',
        'full_or_part_time': 'FullorPartTime',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2015, 9, 9)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'texas_a%26m_university_system/salaries/2015-09/'
           'tamu_2015-09-09.xlsx')

    race_map = {
        '1': 'White (Not Hispanic or Latino)',
        '2': 'Black or African American',
        '3': 'Hispanic or Latino',
        '4': 'Asian',
        '5': 'American Indian or Alaskan Native',
        '6': 'Native Hawaiian or Other Pacific Islander',
        '7': 'Two or More Races',
        '8': 'Not Specified',
        '': 'Not Specified',
    }

    @property
    def organization(self):
        return {
            'name': self.organization_name,
            'children': self.department_as_child,
            'classification': self.ORGANIZATION_CLASSIFICATION,
        }

    @property
    def description(self):
        rate = self.get_mapped_value('rate')
        rate = rate.rstrip('0').rstrip('.') if '.' in rate else rate
        return '{rate}-month salary'.format(rate=rate)

    @property
    def compensation_type(self):
        full_or_part_time = self.get_mapped_value('full_or_part_time')

        if full_or_part_time == 'F':
            return 'FT'

        return 'PT'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def race(self):
        return {
            'name': self.race_map[self.minority_code.strip()]
        }

    def calculate_tenure(self):
            hire_date_data = map(int, self.hire_date.split('-'))
            hire_date = date(hire_date_data[0], hire_date_data[1],
                             hire_date_data[2])
            tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
            if tenure < 0:
                tenure = 0
            return tenure

transform = base.transform_factory(TransformedRecord)
