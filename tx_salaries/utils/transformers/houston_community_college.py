from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department',
        'job_title': 'Position Title',
        'hire_date': 'Original Hire Date',
        'compensation': 'Salary',
        'gender': 'Sex',
        'ethnic_group': 'Ethnic Grp',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Houston Community College'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    DATE_PROVIDED = date(2014, 6, 2)

    URL = "http://raw.texastribune.org.s3.amazonaws.com/houston_community_college/salaries/2014-06/0812_Database.xls"

    gender_map = {'Female': 'F', 'Male': 'M'}

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        # TODO some job titles have PT
        return 'FT'

    @property
    def description(self):
        return 'Annual compensation'

    @property
    def person(self):
        data = {
            'family_name': self.last_name.strip(),
            'given_name': self.first_name.strip(),
            'name': self.get_name(),
        }
        try:
            data.update({
                'gender': self.gender_map[self.gender.strip()]
            })
            return data
        except KeyError:
            return data

    @property
    def race(self):
        if self.ethnic_group.strip() == '':
            self.ethnic_group = 'Not given'
        return {
            'name': self.ethnic_group
        }

transform = base.transform_factory(TransformedRecord)
