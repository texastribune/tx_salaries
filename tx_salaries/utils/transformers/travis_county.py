from datetime import date

from . import base
from . import mixins

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last name',
        'first_name': 'First name',
        'department': 'Personnel Area',
        'job_title': 'Position Title',
        'hire_date': 'Most Recen',
        'employee_type': 'Emp Group',
        'status': 'Emp Sub-Group',
        'gender': 'Gender',
        'given_race': 'Ethnic Origin',
        'compensation': 'Annual Sal',
        'rate': 'Hourly Rat',
    }

    gender_map = {'Female': 'F', 'Male': 'M'}

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Travis County'

    ORGANIZATION_CLASSIFICATION = 'County'

    DATE_PROVIDED = date(2015, 10, 13)

    URL = ('http://s3.amazonaws.com/raw.texastribune.org/travis_county/'
        'salaries/2015-10/traviscounty.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        status = self.status

        if 'Full time' in status:
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        status = self.status
        employee_type = self.employee_type

        if 'Full' in status:
            return 'Annual salary'

        if 'Part' in status:
            return 'Part-time annual salary'

        if 'Hourly' in status:
            return 'Hourly rate'

        if 'Seasonal' in status:
            return 'Hourly rate'

        if 'Fee' in status:
            return 'Stipend'

    @property
    def compensation(self):
        salary = self.get_mapped_value('compensation')
        rate = self.rate

        if salary == '0':
            return self.get_mapped_value('compensation')
        else:
            return self.get_mapped_value('rate')

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    @property
    def race(self):
        race = self.given_race.strip()
        if race == '':
            race = 'Not given'
        return {'name': race}

transform = base.transform_factory(TransformedRecord)
