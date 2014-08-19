from datetime import date

from . import base
from . import mixins

# --sheet=sheet1


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
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

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2014, 1, 16)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_health_tyler/salaries/2014-01/Texas%20Tribune%20-%20UTHSCT%2002054%201-16-2014.xls'

    description = 'Annual compensation'

    @property
    def is_valid(self):
        # be sure to use --sheet="sheet1"

        # Adjust to return False on invalid fields.  For example:
        try:
            return self.hire_date.strip() != ''
        except AttributeError:
            return False

    @property
    def compensation_type(self):
        if self.FTE.strip() == "1.0":
            return 'FT'
        else:
            return 'PT'
        # TODO ask about FTE, FTSA and Annual Rt

transform = base.transform_factory(TransformedRecord)