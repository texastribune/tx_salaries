from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
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

    NAME_FIELDS = ('first_name', 'last_name', )

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
        race = self.given_race.strip()
        if race == '':
            race = 'Not given'
        return {'name': race}


transform = base.transform_factory(TransformedRecord)
