from . import base
from . import mixins
from unicodedata import numeric

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
        'job_title': 'Name of Position',
        'department': 'Department',
        'race': 'Race',
        'gender': 'Gender',
        'employee_type': 'FT/Temp',
        'hire_date': 'Hire Date',
        'compensation': 'Budgeted Annual Salary',
        'compensation_hourly': 'Temp Empl Hourly Rate of Pay'

    }

    ORGANIZATION_NAME = 'Tarrant County'

    ORGANIZATION_CLASSIFICATION = 'County'

    compensation_type = 'FT'

    description = 'Annual rate'

    DATE_PROVIDED = date(2018, 8, 13)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/tarrant_county/salaries/2018-12/tx_tribune.xls')

    gender_map = {'Female': 'F', 'Male': 'M'}

    def get_raw_name(self):
        split_name = self.full_name.split(', ')

        return u' '.join([split_name[1], split_name[0]])

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
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'FT':
            return 'FT'

        if employee_type == 'Temp':
            return 'PT'

    @property
    def compensation(self):
        compensation = self.get_mapped_value('compensation').replace(',', '')
        compensation_hourly = self.get_mapped_value('compensation_hourly').replace(',', '')

        if compensation != '':
            return compensation
        elif compensation_hourly != '':
            return compensation_hourly

    @property
    def description(self):
        compensation = self.get_mapped_value('compensation').replace(',', '')
        compensation_hourly = self.get_mapped_value('compensation_hourly').replace(',', '')

        if compensation != '':
            return 'Annual compensation'
        elif compensation_hourly != '':
            return 'Hourly pay'


transform = base.transform_factory(TransformedRecord)
