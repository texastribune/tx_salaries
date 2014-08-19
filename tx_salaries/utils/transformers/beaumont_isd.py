from . import base
from . import mixins

from datetime import date

# add if necessary: --sheet="Request data" --row=3


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'PER_LAST_NAME',
        'first_name': 'PER_FIRST_NAME',
        'middle_name': 'PER_MIDDLE_NAME',
        'department': 'ORG_NAME',
        'job_title': 'ROLE_NAME',
        'hire_date': 'EMP_HIRE_DT',
        'compensation': 'EMP_ASGN_PAY_HIST_A_NRML_PAY',
        'gender': 'PER_GENDER',
        'race': 'PRIMARY_ETHNICITY_CODE',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Beaumont ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    compensation_type = 'FT'

    description = 'Annual salary'

    DATE_PROVIDED = date(2014, 7, 15)
    # Y/M/D agency provided the data

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/beaumont_isd/salaries/2014-07/FOIA%2014175.xlsx'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def hire_date(self):
        return self.get_mapped_value('hire_date').split('T')[0]

    @property
    def get_raw_name(self):
        middle_name_field = self.middle_name.strip()

        if middle_name_field == '' or middle_name_field == '(null)':
            self.NAME_FIELDS = ('first_name', 'last_name', )

        name_fields = [getattr(self, a).strip() for a in self.NAME_FIELDS]
        return u' '.join(name_fields)

transform = base.transform_factory(TransformedRecord)
