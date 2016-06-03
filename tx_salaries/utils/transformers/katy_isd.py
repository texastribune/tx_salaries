from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Location',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'Salary',
        'employee_type': 'Part Time Full Time',
        'gender': 'Gender',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Katy ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2016, 5, 26)
    # Y/M/D agency provided the data

    # TODO
    URL = "http://raw.texastribune.org.s3.amazonaws.com/katy_isd/salaries/2016-05/PIR%2015524-30-E%20%20Employee%20list.xlsx"

    description = 'Annual compensation'

    ethnicity_choices = ['American Indian', 'Asian', 'Black', 'White',
                         'Pacific Islander', 'Hispanic Ethnicity']

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def race(self):
        ethnicities = []
        for choice in self.ethnicity_choices:
            if self.data[choice] == "Y":
                ethnicities.append(choice)
        ethnicity = " ".join(ethnicities)
        if ethnicity == '':
            ethnicity = 'Not given'
        return {
            'name': ethnicity.strip()
        }

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Full Time':
            return 'FT'

        if employee_type == 'Part Time':
            return 'PT'

    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('/'))
        hire_date = date(hire_date_data[2], hire_date_data[0],
                         hire_date_data[1])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            return 0
        return tenure

    @property
    def post(self):
        return {'label': self.job_title.strip()}

    @property
    def department_as_child(self):
        return [{'name': self.department.strip(), }, ]

transform = base.transform_factory(TransformedRecord)
