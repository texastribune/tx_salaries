from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin,
        mixins.GenericJobTitleMixin,
        mixins.MembershipMixin,
        mixins.OrganizationMixin,
        mixins.PostMixin,
        base.BaseTransformedRecord):
    MAP = {
        'department': 'Department ',
        'name': 'Name',
        'job_title': 'Title',
        'last_name': 'Last Name',
        'hire_date': 'Hire Date',
        'pay_status': 'FT or PT Status',
        'compensation': 'Annual Salary',
        'race': 'Race',  # Not used yet, need to allow multiple
        'system_status': 'COA',
    }

    NAME_FIELDS = ('name', )
    ORGANIZATION_NAME = 'Texas Tech University{suffix}'

    # The data we get for Texas Tech System is always valid
    is_valid = True

    # All employees are full-time right now
    compensation_type = 'Full Time'

    @property
    def is_system(self):
        return self.system_status == 'S'

    @property
    def organization_name(self):
        suffix = ' System' if self.is_system else ''
        return self.ORGANIZATION_NAME.format(suffix=suffix)

    @property
    def organization(self):
        return {
            'name': self.organization_name,
            'children': self.department_as_child,
        }

    @property
    def identifier(self):
        """
        Identifier by Texas Tech Systems

        Ignore everything but name/gender.  We have not found any
        duplicate name gender records (yet), and should not as TT
        includes middle initials.
        """
        excluded = [self.race_key, self.department_key, self.job_title_key,
                self.hire_date_key, self.compensation_key,
                self.system_status_key, ]
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                    exclude=excluded)
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


transform = base.transform_factory(record_class=TransformedRecord,
        transform_func=base.generic_merge_cell_transform)
