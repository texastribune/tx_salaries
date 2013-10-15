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


transform = base.transform_factory(TransformedRecord)
