from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Rehire Dt',
        'status': 'LABEL FOR FT/PT STATUS',
        'compensation': 'Annual Rt',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas Health Science Center at Tyler'

    # All employees are full-time right now
    compensation_type = 'Full Time'

    @property
    def is_valid(self):
        #it's the wrong sheet!

        # Adjust to return False on invalid fields.  For example:
        try:
            return self.hire_date.strip() != ''
        except AttributeError:
            return False


transform = base.transform_factory(TransformedRecord)
