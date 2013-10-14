from copy import copy

from . import base
from . import mixins


def title_case_property(key):
    return property(lambda self: self.get_mapped_value(key).title())


class TransformedRow(mixins.OrganizationMixin, mixins.PostMixin,
        base.BaseTransformedRow):
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

    department = title_case_property('department')
    job_title = title_case_property('job_title')

    @property
    def identifier(self):
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_row(self.data,
                    exclude=[self.compensation_key, ])
        }

    @property
    def person(self):
        name = self.get_name()
        return {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
        }

    # TODO Refactor into a mixin
    @property
    def membership(self):
        return {
            'start_date': self.hire_date,
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


def transform_row(row):
    obj = TransformedRow(row)
    # Stop early if this isn't valid
    if not obj.is_valid:
        return

    d = copy(base.DEFAULT_DATA_TEMPLATE)
    d['original'] = row

    d['tx_people.Identifier'] = obj.identifier
    d['tx_people.Person'] = obj.person
    d['tx_people.Organization'] = obj.organization
    d['tx_people.Post'] = obj.post
    d['tx_people.Membership'] = obj.membership
    d['compensations'] = obj.compensations
    return d


def transform(labels, source):
    data = []
    for raw_row in source:
        row = dict(zip(labels, raw_row))
        processed = transform_row(row)
        if processed:
            data.append(processed)
    return data
