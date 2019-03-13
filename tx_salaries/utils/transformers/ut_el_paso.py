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
        'first_name': 'First Name',
        'last_name': 'Last',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Start Date',
        'compensation': 'Annual Rt',
        'employee_type': 'Full/Part',
        'gender': 'Sex',
        'nationality': 'Descr'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at El Paso'

    ORGANIZATION_CLASSIFICATION = 'University'

    description = 'Annual rate'

    DATE_PROVIDED = date(2018, 9, 25)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_el_paso/salaries/2018-09/TPIA.xlsx'

    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

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
    def race(self):
        if self.nationality.strip() == '':
            self.nationality = 'Not given'
        return {
            'name': self.nationality
        }

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return 'FT'

        if employee_type == 'P':
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return "Annual salary"

        if employee_type == 'P':
            return "Part-time annual salary"

transform = base.transform_factory(TransformedRecord)
