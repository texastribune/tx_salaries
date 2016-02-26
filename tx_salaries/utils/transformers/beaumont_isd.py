from . import base
from . import mixins

from datetime import date

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LNAME',
        'first_name': 'FNAME',
        'department': 'DEPT',
        'job_title': 'TITLE',
        'hire_date': 'HIREDATE',
        'compensation': 'BUDGETED_SALARY',
        'gender': 'SEX',
        'race': 'Race',
        'employee_type': 'Status'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Beaumont ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    compensation_type = 'FT'

    description = 'Budgeted salary'

    DATE_PROVIDED = date(2016, 2, 26)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/beaumont_isd/salaries/2016-02/beaumontisd.xlsx'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def hire_date(self):
        return self.get_mapped_value('hire_date').split('T')[0]

    def get_raw_name(self):
        middle_name_field = self.middle_name.strip()

        if middle_name_field == '' or middle_name_field == '(null)':
            self.NAME_FIELDS = ('first_name', 'last_name', )

        name_fields = [getattr(self, a).strip() for a in self.NAME_FIELDS]
        return u' '.join(name_fields)

transform = base.transform_factory(TransformedRecord)
