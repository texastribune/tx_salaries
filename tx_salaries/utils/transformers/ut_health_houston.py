from datetime import date

from . import base
from . import mixins

# http://raw.texastribune.org.s3.amazonaws.com/ut_health_houston/salaries/2014-01/Employee%20Salary%201-29-2014%20%282%29.xls


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
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

    DATE_PROVIDED = date(2014, 1, 29)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''


transform = base.transform_factory(TransformedRecord)
