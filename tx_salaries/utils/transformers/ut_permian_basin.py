from . import base
from . import mixins

from datetime import date


class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Start Date',
        'compensation': 'Annual Rt',
        'gender': 'Sex',
        'given_race': 'Race',
        'employee_type': 'Full/Part',
    }

    ORGANIZATION_NAME = 'University of Texas of the Permian Basin'

    ORGANIZATION_CLASSIFICATION = 'Universtiy'

    DATE_PROVIDED = date(2016, 2, 29)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/ut_permian_basin'
           '/salaries/2016-02/ut_permbasin.xls')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('employee_type')

        if 'Full' in emptype:
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        emptype = self.get_mapped_value('employee_type')

        if 'Full' in emptype:
            return 'Annual rate'
        else:
            return 'Part-time annual rate'

    @property
    def person(self):
        formatted_name = self.get_name()

        r = {
            'family_name': formatted_name['last_name'],
            'given_name': formatted_name['first_name'],
            'name': " ".join([n for n in formatted_name.values()]),
            'gender': self.gender.strip()
        }

        return r

    def get_name(self):
        last_name = self.get_mapped_value('last_name')
        first_name = self.get_mapped_value('first_name').title()
        return {
            'first_name': first_name,
            'last_name': last_name
        }

    @property
    def race(self):
        race = self.given_race.strip()
        if race == '':
            race = 'Not given'
        return {'name': race}


transform = base.transform_factory(TransformedRecord)
