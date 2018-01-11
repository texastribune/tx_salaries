from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LastName',
        'first_name': 'FirstName',
        'middle_name': 'MiddleName',
        'department': 'DEPARTMENT',
        'job_title': 'JobTitle',
        'gender': 'Gender',
        'race': 'Ethnicity',
        'hire_date': 'JobBeginDate',
        'compensation': 'JobAnnualSalary',
        'employee_type': 'JobFTE',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    gender_map = {'Female': 'F', 'Male': 'M'}

    ORGANIZATION_NAME = 'Texas Southern University'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2017, 5, 15)

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/ut_medical_branch/'
            'salaries/2017-05/utmb.xlsx')

    @property
    def compensation_type(self):

        if self.employee_type < 1:
            return 'PT'
        else:
            return 'FT'

    @property
    def description(self):

        if self.employee_type < 1:
            return "Part-time annual compensation"
        else:
            return "Annual compensation"

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def person(self):
        data = {
            'family_name': self.last_name,
            'given_name': self.first_name,
            'name': self.get_raw_name(),
            'gender': self.gender_map[self.gender.strip()]
        }

        return data


transform = base.transform_factory(TransformedRecord)
