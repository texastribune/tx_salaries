from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'NAME LAST',
        'first_name': 'NAME FIRST',
        'department': 'DEPARTMENT TITLE',
        'job_title': 'JOB TITLE',
        'hire_date': 'CONTINUOUS EMPLOYMENT DATE',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'status': 'LABEL FOR FT/PT STATUS',
        'compensation': 'FY ALLOCATIONS',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at Austin'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given, 29 < 4000
    compensation_type = 'Full Time'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    def process_hire_date(self, hire_date):
        #19 cases
        if hire_date.strip() == "":
            return ""
        year = hire_date[0:4]
        month = hire_date[4:6]
        day = hire_date[6:8]
        return "-".join([year, month, day])

    @property
    def compensations(self):
        hire_date = self.process_hire_date(self.hire_date)
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': hire_date,
                    'compensation': self.compensation,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
            }
        ]

transform = base.transform_factory(TransformedRecord)
