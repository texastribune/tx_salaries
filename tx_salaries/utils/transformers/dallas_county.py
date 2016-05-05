from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'LAST_NAME',
        'first_name': 'FIRST_NAME',
        'department': 'ORGANIZATION_NAME',
        'job_title': 'JOB_NAME',
        'hire_date': 'LAST_HIRE_DATE',
        'status': 'EMPLOYMENT_CATEGORY',
        'compensation': 'SALARY_AMOUNT',
        'gender': 'SEX',
        'race': 'ETHNIC',
        'basis': 'SALARY_BASIS'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Dallas County'

    ORGANIZATION_CLASSIFICATION = 'County'

    DATE_PROVIDED = date(2016, 4, 7)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas_county/salaries/2016-04/dallas-county.xls')

    basis_map = {
        'EXEMPT': '',
        'NON-EXEMPT': 'hourly'
    }
    category_map = {
        'FR': 'Full Time Regular',
        'PT': 'Part Time Temporary',
        'PR': 'Part Time Regular',
        'PB': 'Part Time with Benefits'
    }

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    def process_compensation_description(self):
        basis = self.basis_map[self.basis.upper()]
        category = self.category_map[self.status.upper()]
        category_basis = " ".join([category, basis]).strip()
        return category_basis

    def process_compensation(self):
        if self.basis.upper() == 'EXEMPT':
            return float(self.compensation) * 12
        else:
            return self.compensation

    @property
    def compensations(self):
        # TODO: ADJUST HOUR PAY
        compensation_description = self.process_compensation_description()
        compensation = self.process_compensation()
        compensation_type = 'FT' if compensation_description == 'Full Time Regular' else 'PT'
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': compensation_type,
                    'description': compensation_description
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': compensation,
                    'tenure': self.calculate_tenure()
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
            }
        ]

transform = base.transform_factory(TransformedRecord)
