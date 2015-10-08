from datetime import date

from . import base
from . import mixins

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'AMIND': 'American Indian',
        'ASIAN': 'Asian',
        'BLACK': 'Black',
        'HISPA': 'Hispanic',
        'NSPEC': 'Unspecified',
        'PACIF': 'Pacific Islander',
        'WHITE': 'White',
        'gender': 'Gender',
        'compensation': 'Rate',
        'employment_type': 'Full/Part',
        'employment_frequency': 'Freq',
        'hours': 'Stnd Hrs/Wk'
    }

    gender_map = {'Female': 'F', 'Male': 'M', 'Unknown': 'U'}

    ORGANIZATION_NAME = 'University of Texas at San Antonio'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2015, 10, 7)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/ut_san_antonio/'
            'salaries/2015-10/utsanantonio.xls')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != '' and self.hire_date.strip() != ''

    @property
    def compensation_type(self):
        emp_type = self.employment_type

        if emp_type == 'F':
            return 'FT'

        if emp_type == 'P':
            return 'PT'

    @property
    def description(self):
        freq = self.employment_frequency

        if freq == 'A':
            return "Full-time salary"

        if freq == 'H':
            return "Hourly rate"

        if freq == 'C':
            return "Contract salary"


    @property
    def compensations(self):
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                    'description': self.description
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                    'tenure': self.calculate_tenure(),
                },
                'tx_salaries.EmployeeTitle': {
                    'name': unicode(cleaver.DepartmentNameCleaver(self.job_title)
                                           .parse())
                },
            }
        ]

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

    def get_raw_name(self):
        split_name = self.full_name.split(',')
        last_name = split_name[0]
        split_firstname = split_name[1].split(' ')
        first_name = split_firstname[0]
        if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
            middle_name = split_firstname[1]
        else:
            first_name = split_name[1]
            middle_name = ''

        return u' '.join([first_name, middle_name, last_name])


transform = base.transform_factory(TransformedRecord)
