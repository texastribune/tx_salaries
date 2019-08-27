from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord)::

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'employee_type': 'Full-time or Part-time',
        'gender': 'Gender',
        'given_race': 'Race/Ethinicity',
        'compensation': 'Annual Salary Rate',
    }

    gender_map = {
        'Female':'F',
        'Male':'M',
        '': 'Unknown'
    }

    NAME_FIELDS = ('full_name', )
    ORGANIZATION_NAME = 'University of Texas at Austin'
    ORGANIZATION_CLASSIFICATION = 'University'
<<<<<<< HEAD
    DATE_PROVIDED = date(2019, 7, 30)
=======
    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    DATE_PROVIDED = date(2017, 7, 6)

>>>>>>> 33654245d3f21b1ea97778d42091c22cf57e5a4d
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
        'ut_austin/salaries/2019-07/employee_data.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def race(self):
        race = self.given_race.strip()

        if race == '':
            race = 'Unknown'
        return {
            'name': race
        }

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
        employee_type = self.employee_type

        if employee_type == 'Full-time':
            return 'FT'

        if employee_type == 'Part-time':
            return 'PT'

    @property
    def description(self):
        return "Annual salary rate"


transform = base.transform_factory(TransformedRecord)
