from datetime import date

import string

from . import base
from . import mixins


class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericIdentifierMixin,
    mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last name',
        'first_name': 'First name',
        'department_name': 'Personnel Area',
        'job_title': 'Position Title',
        'hire_date': 'Most Recent Hire Dt.',
        'status': 'Emp Sub-Group',
        'gender_type': 'Gender',
        'given_race': 'Ethnicity',
        'compensation': 'Annual Salary',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Travis County'

    ORGANIZATION_CLASSIFICATION = 'County'

    DATE_PROVIDED = date(2017, 4, 21)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'travis_county/salaries/2017-05/'
           'PIR.xlsx')

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
            'name': unicode(name),
            'gender': self.get_mapped_value('gender_type')
        }

        return r

    @property
    def gender(self):
        gender = self.get_mapped_value('gender_type')
        
        if gender.strip() == '':
            return 'Not Given'
        else:
            return gender

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('status')

        if 'Full' in emptype:
            return 'FT'
        elif 'Part' in emptype:
            return 'PT'

    @property
    def description(self):
        status = self.status

        if 'Full' in status:
            return 'Annual salary'
        elif 'Part' in status:
            return 'Part-time, annual salary'

    @property
    def race(self):
        race = self.given_race.strip()

        if race == '':
            race = 'Not given'
        
        return {'name': race}

    @property
    def department(self):
        dept = self.department_name.strip()

        if dept == 'Health and Human Sv and Vet Sv':
            dept = 'Health & Human Services and Veterans Services'
        elif dept == 'Counseling And Education Sv':
            dept = 'Counseling & Education Services'
        elif dept == 'Transportation And Nat Rsrc':
            dept = 'Transportation & Natural Resources'
        elif dept == 'Rcd Mgmt And Comm Rsrc':
            dept = 'Records Management Communications Resources'

        return dept

transform = base.transform_factory(TransformedRecord)
