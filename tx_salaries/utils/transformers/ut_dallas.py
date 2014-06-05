import re

from . import base
from . import mixins

from datetime import date

# http://raw.texastribune.org.s3.amazonaws.com/ut_dallas/salaries/2014-02/FOIA%20Request%20-%20Tribune.xlsx

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Department',
        'job_title': 'Job Description',
        'hire_date': 'Start Date',
        'race': 'Ethnic Group',
        'gender': 'Sex',
        'status': 'LABEL FOR FT/PT STATUS',
        'compensation': 'Annual Rate if Applicable',
        'hourly': 'Hourly Rate if Applicable'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at Dallas'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2014, 2, 19)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        if self.compensation.strip() != '':
            return 'Full Time'
        else:
            # TODO need hours worked
            return 'Part Time'

    @property
    def compensations(self):
        comp = self.compensation if self.compensation.strip() != '' else self.hourly
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': comp,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
            }
        ]

transform = base.transform_factory(TransformedRecord)
