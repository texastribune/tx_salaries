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
        'last_name': 'Last',
        'first_name': 'First',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'status': 'Status',
        'contract': 'Months of Contract',
        'gender': 'Gender',
        'given_race': 'Race',
        'compensation': 'Salary',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Tarrant County College'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    DATE_PROVIDED = date(2015, 11, 13)

    URL = ('http://s3.amazonaws.com/raw.texastribune.org/tarrant_county_college/'
        'salaries/2015-11/tarrantcountycollege.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('status')

        if emptype == 'Full Time' or emptype == 'Temporary Full Time':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        status = self.status
        contract = float(self.contract)

        if status == 'Part Time':
            return 'Hourly rate'
        elif status == '60% Full Time':
            return 'Part time salary'
        else:
            return '{0:g}'.format(contract) + '-month salary'

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
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
