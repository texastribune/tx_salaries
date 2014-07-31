from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LAST NAME',
        'first_name': 'FIRST NAME',
        'middle_name': 'MIDDLE NAME',
        'department': 'LOCATION NAME',
        'job_title': 'JOB DESCRIPTION',
        'classification': 'JOB CLASSIFICATION',
        'hire_date': 'HIRE DATE',
        'compensation': 'SALARY',
        'gender': 'SEX',
        'race': 'RACE',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Pasadena ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2014, 5, 27)
    # Y/M/D agency provided the data

    compensation_type = 'FT'
    description = 'Annual compensation'

    URL = "http://raw.texastribune.org.s3.amazonaws.com/pasadena_isd/salaries/2014-05/Pasadena%20ISD%20Employees.xls"

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != '' and self.classification.strip() != ''

    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('/'))
        hire_date = date(hire_date_data[2], hire_date_data[0],
                         hire_date_data[1])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            tenure = 0
        return tenure

    @property
    def post(self):
        return {'label': self.job_title.strip()}

    @property
    def department_as_child(self):
        return [{'name': self.department.strip(), }, ]

transform = base.transform_factory(TransformedRecord)
