from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Name - Last Name',
        'middle_name': 'Name - Middle Name',
        'first_name': 'Name - First Name',
        'department': 'Department',
        'job_title': 'Emp Type Code',
        'hire_date': 'Hire Date',
        'compensation': 'Actual Calc\' Contract Pay',
        'race': 'Race Desc',
        'gender': 'Gender',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Eanes ISD'
    ORGANIZATION_CLASSIFICATION = 'School District'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        return 'Full Time'

    @property
    def compensation(self):
        raw = self.get_mapped_value('compensation')
        return raw.strip(' $').replace(',', '')

transform = base.transform_factory(TransformedRecord)
