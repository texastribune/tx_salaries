from datetime import date

from . import base
from . import mixins

# http://raw.texastribune.org.s3.amazonaws.com/ut_medical_branch/salaries/2014-01/Texas%20Tribune%20Salary%20PIA.xlsx


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'FAMILY_NAME',
        'first_name': 'GIVEN_NAME',
        'department': 'DEPARTMENT',
        'job_title': 'JOBTITLE',
        'gender': 'GENDER',
        'race': 'RACE/ETHNICITY',
        'hire_date': 'LAST_HIRE_DT',
        'compensation': 'ANNUAL_PAY',
        'longevity': 'ANNUALIZED_LONGEVITY'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    gender_map = {'Female': 'F', 'Male': 'M'}

    ORGANIZATION_NAME = 'The University of Texas Medical Branch at Galveston'

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    # TODO not given on spreadsheet, but they appear to give part time
    compensation_type = 'Full Time'

    DATE_PROVIDED = date(2014, 1, 27)

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
        }
        try:
            data.update({
                'gender': self.gender_map[self.gender.strip()]
            })
            return data
        except KeyError:
            return data

    def process_compensation(self):
        #TODO longevity is in addition to base annual_pay, add if applicable
        if self.longevity.strip() == '0':
            return self.compensation
        else:
            longevity = self.longevity.strip().replace(',', '')
            salary = self.compensation.strip().replace(',', '')
            return float(salary) + float(longevity)

    @property
    def compensations(self):
        compensation = self.process_compensation()
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': compensation,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
            }
        ]


transform = base.transform_factory(TransformedRecord)
