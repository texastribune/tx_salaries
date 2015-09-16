from datetime import date

from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'gender': 'Sex',
        'race': 'Ethnic Grp',
        'hire_date': 'Start Date',
        'compensation': 'Total Comp Rate',
        'compensation_type': 'Full/Part',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'The University of Texas Health Science Center at Houston'

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # TODO not given on spreadsheet, but they appear to give part time

    @property
    def compensation_type(self):
        if self.get_mapped_value('compensation_type') == 'F':
            return 'FT'
        elif self.get_mapped_value('compensation_type') == 'P':
            return 'PT'
        else:
            return ''

    description = 'Annual compensation' # Should still be called annual compenstation?

    DATE_PROVIDED = date(2015, 8, 10)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_health_houston/salaries/2015-08/ut_health_science_center_houston.xlsx'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''


transform = base.transform_factory(TransformedRecord)
