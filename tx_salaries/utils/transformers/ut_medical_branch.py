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
        'last_name': 'FAMILY_NAME',
        'first_name': 'GIVEN_NAME',
        'department': 'DEPARTMENT',
        'job_title': 'JOBTITLE',
        'gender': 'GENDER',
        'race': 'ETHNIC_GROUP_DESCR',
        'hire_date': 'LAST_HIRE_DT',
        'compensation': 'ANNUAL_PAY',
        'longevity': 'ANNUALIZED_LONGEVITY',
        'employee_type': 'FULL_PART_TIME',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    gender_map = {'Female': 'F', 'Male': 'M'}

    ORGANIZATION_NAME = 'The University of Texas Medical Branch at Galveston'

    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2017, 5, 15)

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/ut_medical_branch/'
            'salaries/2017-05/utmb.xlsx')

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
        #longevity is in addition to base annual_pay, add if applicable
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
