from . import base
from . import mixins

from datetime import date
from .. import cleaver


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
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

    DATE_PROVIDED = date(2018, 5, 8)
    # Y/M/D agency provided the data

    # TODO
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'katy_isd/salaries/2018-05/pir.xlsx')

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
                if choice == 'Hispanic Ethnicity':
                    ethnicities.append('Hispanic')
                else:
                    ethnicities.append(choice)
        ethnicity = ", ".join(ethnicities)
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

    @property
    def hire_date(self):
        raw_date = self.get_mapped_value('hire_date')

        return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

    @property
    def post(self):
        return {'label': self.job_title.strip()}

    @property
    def department_as_child(self):
        return [{'name': self.department.strip(), }, ]

transform = base.transform_factory(TransformedRecord)
