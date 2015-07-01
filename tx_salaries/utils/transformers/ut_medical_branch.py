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
        'last_name': 'FAMILY NAME',
        'first_name': 'GIVEN NAME',
        'department': 'DEPARTMENT',
        'job_title': 'JOBTITLE',
        'gender': 'GENDER',
        'race': 'RACE/ETHNICITY',
        'hire_date': 'LAST HIRE DATE',
        'compensation': 'ANNUAL PAY',
        'longevity': 'ANNUALIZED LONGEVITY',
        'employee_type': 'FULL/PART TIME',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    gender_map = {'Female': 'F', 'Male': 'M'}

    ORGANIZATION_NAME = 'The University of Texas Medical Branch at Galveston'

    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2015, 6, 24)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/ut_medical_branch/'
            'salaries/2015-06/ut_medical_galveston.xlsx')

    @property
    def compensation_type(self):

        if self.employee_type == 'Part-time':
            return 'PT'
        else:
            return 'FT'

    @property
    def description(self):

        if self.employee_type == 'Part-time':
            return "Part-time annual compensation"
        else:
            return "Annual compensation"

    @property
    def compensation(self):
        if self.get_mapped_value('longevity') == '0':
            return self.get_mapped_value('compensation')
        else:
            longevity = self.get_mapped_value('longevity')
            salary = self.get_mapped_value('compensation')
            return float(salary) + float(longevity)

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
