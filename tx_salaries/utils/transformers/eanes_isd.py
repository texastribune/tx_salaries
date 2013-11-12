from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Name - Last Name',
        'middle_name': 'Name - Middle Name',
        'first_name': 'Name - First Name',
        'department': 'Department',
        'job_title': 'Emp Type Code',
        'hire_date': 'Hire Date',
        'compensation': 'Actual Calc Contract Pay',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Eanes ISD'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        if self.status.upper() == 'FT':
            return 'Full Time'
        else:
            return 'Part Time'

    @property
    def compensation(self):
        raw = self.get_mapped_value('compensation')
        # TODO: clean the raw variable
        cleaned = raw
        return cleaned

transform = base.transform_factory(TransformedRecord)
