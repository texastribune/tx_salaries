from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericIdentifierMixin,
    mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LAST_NAME',
        'first_name': 'FIRST_NAME',
        'department': 'ORGANIZATION_NAME',
        'job_title': 'JOB_NAME',
        'hire_date': 'LAST_HIRE_DATE',
        'status': 'EMPLOYMENT_CATEGORY',
        'compensation': 'ANNUAL',
        'gender': 'SEX',
        'race': 'ETHNIC',
        # 'basis': 'SALARY_BASIS'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'Dallas County'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'County'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2018, 1, 22)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas_county/salaries/2018-01/TX_TRIBUNE_1_2018.xlsx')

    # basis_map = {
    #     'EXEMPT': '',
    #     'NON-EXEMPT': 'Hourly'
    # }

    category_map = {
        'FR': 'Full Time',
        'PR': 'Part Time (More than 20, less than 30 hours per week)',
        'PB': 'Part Time (More than 230 hours per week)',
        'PT': 'Part Time (Less than 20 hours per week/seasonal)'
    }

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def person(self):
        name = self.get_name()

        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

    @property
    def description(self):
        return self.category_map[self.status.upper()]

    @property
    def compensation_type(self):
        emp_type = self.status

        if emp_type == 'FR':
            return 'FT'
        else:
            return 'PT'

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')


    # def process_compensation_description(self):
    #     basis = self.basis_map[self.basis.upper()]
    #     category = self.category_map[self.status.upper()]
    #     category_basis = " ".join([category, basis]).strip()
    #     return category_basis

    # def process_compensation(self):
    #     if self.basis.upper() == 'EXEMPT':
    #         return float(self.compensation) * 12
    #     else:
    #         return self.compensation

    # @property
    # def compensations(self):
    #     # TODO: ADJUST HOUR PAY
    #     compensation_description = self.process_compensation_description()
    #     compensation = self.process_compensation()
    #     compensation_type = 'FT' if compensation_description == 'Full Time Regular' else 'PT'
    #     return [
    #         {
    #             'tx_salaries.CompensationType': {
    #                 'name': compensation_type,
    #                 'description': compensation_description
    #             },
    #             'tx_salaries.Employee': {
    #                 'hire_date': self.hire_date,
    #                 'compensation': compensation,
    #                 'tenure': self.calculate_tenure()
    #             },
    #             'tx_salaries.EmployeeTitle': {
    #                 'name': self.job_title,
    #             },
    #         }
    #     ]

transform = base.transform_factory(TransformedRecord)
