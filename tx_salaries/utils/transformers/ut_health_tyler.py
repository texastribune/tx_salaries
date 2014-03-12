from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Rehire Dt',
        'gender': 'Sex',
        'race': 'Ethnic Grp',
        'status': 'LABEL FOR FT/PT STATUS',
        'compensation': 'Annual Rt',
        'FTE': 'FTE'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas Health Science Center at Tyler'

    @property
    def is_valid(self):
        #it's the wrong sheet!

        # Adjust to return False on invalid fields.  For example:
        try:
            return self.hire_date.strip() != ''
        except AttributeError:
            return False

    @property
    def compensation_type(self):
        if self.FTE.strip() == "1.0":
            return 'Full Time'
        else:
            return 'Part Time'
        # TODO ask about FTE, FTSA and Annual Rt


transform = base.transform_factory(TransformedRecord)
