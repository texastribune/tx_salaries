from . import base
from . import mixins


class TransformedRecord(mixins.GenericDepartmentMixin,
        mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin,
        mixins.MembershipMixin,
        mixins.OrganizationMixin,
        mixins.PostMixin,
        base.BaseTransformedRecord):
    MAP = {
        'department': 'Department',
        'first_name': 'First Name',
        'job_title': 'Position Title',
        'last_name': 'Last Name',
        'hire_date': 'Hire Date',
        'pay_status': 'FT or PT Status'
    }

    NAME_FIELDS = ('first_name', 'last_name', )
    ORGANIZATION_NAME = 'Alamo College'

    POSSIBLE_COMPENSATION_KEYS = ('FT  or PT Semester Salary', 'Hourly Rate', )

    @property
    def is_valid(self):
        return len(self.pay_status.strip()) > 1

    @property
    def part_time(self):
        return self.pay_status.upper() == 'PT'

    @property
    def full_time(self):
        return not self.part_time

    @property
    def has_hourly_rate(self):
        return bool(self.data['Hourly Rate'].strip())

    @property
    def compensation_key(self):
        return self.POSSIBLE_COMPENSATION_KEYS[int(self.has_hourly_rate)]

    @property
    def compensation(self):
        return self.data[self.compensation_key]

    @property
    def compensation_type(self):
        return '%s Time' % 'Part' if self.part_time else 'Full'

    @property
    def identifier(self):
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                    exclude=self.POSSIBLE_COMPENSATION_KEYS)
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

    @property
    def compensations(self):
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                },
            }
        ]

transform = base.transform_factory(TransformedRecord)
