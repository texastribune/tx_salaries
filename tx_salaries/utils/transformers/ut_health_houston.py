from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'gender': 'Sex',
        'race': 'Ethnic Grp',
        'hire_date': 'Current Hire Date',
        'compensation': 'Total Comp Rate',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'The University of Texas Health Science Center at Houston'

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # TODO not given on spreadsheet, but they appear to give part time
    compensation_type = 'Full Time'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''


transform = base.transform_factory(TransformedRecord)
