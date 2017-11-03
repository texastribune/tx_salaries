from datetime import date

from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'DEPARTMENT',
        'job_title': 'Position Title',
        'hire_date': 'Last Start Date',
        'nationality': 'Ethnicity',
        'gender': 'Gender',
        'compensation': 'Comp Rate',
        'status': 'Status',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas System Administration'

    ORGANIZATION_CLASSIFICATION = 'University'

    # description = 'Annual compensation'

    DATE_PROVIDED = date(2017, 10, 30)

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'ut_system/salaries/2017-10/ut_system.XLS')

    race_map = {
        'WHITE': 'White',
        'BLACK': 'Black',
        'HISPA': 'Hispanic',
        'ASIAN': 'Asian',
        'AMIND': 'American Indian',
        'PACIF': 'Pacific Islander',
        'N/A': 'Not given',
    }

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    @property
    def compensation_type(self):
        status = self.get_mapped_value('status').strip()
        salary = float(self.get_mapped_value('compensation'))
        # The hourly rate threshold is $125. Above that, it's annual salary
        # If an employee is full time and has an hourly rate, they're marked
        # as part-time so they don't screw up the math.
        if salary > 125 and status == 'Full time':
            return "FT"
        elif salary > 125 and status == 'Part time':
            return "PT"
        elif salary <= 125 and status == 'Full time':
            return "PT"
        elif salary <= 125 and status == 'Part time':
            return "PT"

    @property
    def description(self):
        salary = float(self.get_mapped_value('compensation'))
        status = self.get_mapped_value('status').strip()
        # The hourly rate threshold is $125. Above that, it's annual salary
        if salary > 125 and status == 'Full time':
            return "Full-time annual salary"
        elif salary > 125 and status == 'Part time':
            return "Part-time annual salary"

        if salary <= 125 and status == 'Full time':
            return "Full-time hourly rate"
        elif salary <= 125 and status == 'Part time':
            return "Part-time hourly rate"

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


transform = base.transform_factory(TransformedRecord)
