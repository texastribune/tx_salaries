from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'full_name': 'NAME',
        'department': 'SHORT-DEPT',
        'job_title': 'SHORT-TITL',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'hire_date': 'DATE-HIRED',
        'compensation': 'RATE',
        'hourly': 'ACTIVE-GRP'
    }

    ORGANIZATION_NAME = 'The University of Texas at Tyler'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    def process_name(self, name):
        split_name = name.split(',')
        return {
            'given_name': split_name[1].strip(),
            'family_name': split_name[0].strip()
        }

    @property
    def person(self):
        names = self.process_name(self.full_name)
        data = {
            'family_name': names['family_name'],
            'given_name': names['given_name'],
            'name': " ".join([names['family_name'], names['given_name']]),
            'gender': self.gender,
        }
        return data

    @property
    def compensation_type(self):
        # TODO ask why self.hourly given as ACTIVE-HOURLY or ACTIVE
        if self.hourly == 'ACTIVE':
            return 'Full Time'
        else:
            return 'Part Time'


transform = base.transform_factory(TransformedRecord)
