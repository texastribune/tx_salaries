from copy import copy

from . import base
from . import mixins


class TransformedRecord(mixins.GenericDepartmentMixin,
        mixins.GenericIdentifierMixin, mixins.GenericJobTitleMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        base.BaseTransformedRecord):
    MAP = {
        'last_name': 'LAST NAME',
        'first_name': 'FIRST NAME',
        'middle_name': 'MI',
        'department': 'CAMPUS/DEPT',
        'job_title': 'POSITION',
        'hire_date': 'HIRE_DATE',
        'compensation': 'SALARY',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Brownsville ISD'

    @property
    def is_valid(self):
        return self.last_name.upper().strip() != 'EMPLOYEE COUNT:'

    @property
    def person(self):
        name = self.get_name()
        return {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
        }

    @property
    def compensations(self):
        # TODO: Is FT Teacher the correct everywhere?
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': 'Full Time Teacher',
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                },
            },
        ]

    def as_dict(self):
        # Stop early if this isn't valid
        if not self.is_valid:
            return

        d = copy(base.DEFAULT_DATA_TEMPLATE)
        d['original'] = self.data

        d['tx_people.Identifier'] = self.identifier
        d['tx_people.Person'] = self.person
        d['tx_people.Organization'] = self.organization
        d['tx_people.Post'] = self.post
        d['tx_people.Membership'] = self.membership
        d['compensations'] = self.compensations
        return d


transform = base.transform_factory(TransformedRecord)
