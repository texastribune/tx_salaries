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
        'department': 'DEPT',
        'job_title': 'Position Title',
        'hire_date': 'DOH',
        'gender': 'Sex',
        'given_race': 'Ethnic',
        'employee_type': 'F/PT',
        'compensation': 'Salary',
    }

    ORGANIZATION_NAME = 'University of Texas of the Permian Basin'

    ORGANIZATION_CLASSIFICATION = 'Universtiy'

    DATE_PROVIDED = date(2017, 11, 21)

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'ut_permian_basin/salaries/2017-11/UTPB_Tribune_Request_11-15-2017.xlsx')

    NAME_FIELDS = ('first_name', 'last_name', )

    race_map = {
        'AMIIND': 'American/Alaska Native',
        'AMIND': ' American/Alaska Native',
        'ASIAN': 'Asian',
        'BLACK': 'Black or African American',
        'PACIF': 'Hawaiian/Pacific Islander',
        'HISPA': 'Hispanic',
        'WHITE': 'White'
    }

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('employee_type')

        if 'F' in emptype:
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        emptype = self.get_mapped_value('employee_type')

        if 'F' in emptype:
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

    # def get_name(self):
    #     last_name = self.get_mapped_value('last_name')
    #     first_name = self.get_mapped_value('first_name').title()
    #     return {
    #         'first_name': first_name,
    #         'last_name': last_name
    #     }

    @property
    def race(self):
        race = self.given_race.strip()
        if race == '':
            race = 'Unknown'
        # return {'name': race}
        return {'name': self.race_map[race]}

    @property
    def department(self):
        dept = self.get_mapped_value('department')

        return dept

    @property
    def job_title(self):
        job = self.get_mapped_value('job_title')

        return job

transform = base.transform_factory(TransformedRecord)
