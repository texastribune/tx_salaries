from . import base
from . import mixins

from datetime import date
from .. import cleaver


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Job Descr',
        'hire_date': 'Start Date',
        'compensation': 'Annual Rt',
        'gender': 'Sex',
        'nationality': 'Ethnic Grp',
    }

    # The name of the organization this WILL SHOW UP ON THE SITE,
    # so double check it!
    ORGANIZATION_NAME = 'University of Houston'

    # What type of organization is this?
    # This MUST match what we use on the site,
    # double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    compensation_type = 'FT'

    description = 'Annual salary'

    race_map = {
        'AMIND': 'American Indian/Alaska Native',
        'WHITE': 'White',
        'HISPA': 'Hispanic/Latino',
        'ASIAN': 'Asian',
        '2+RACE': 'Mixed race',
        'PACIF': 'Native Hawaiian/Other Pacific Islander',
        'BLACK': 'Black/African American',
        'NSPEC': 'Not Specified',
        # Needs verification from UH
        'NHISP': 'White',
        '': 'Not given',
    }

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    DATE_PROVIDED = date(2015, 4, 30)
    # Y/M/D agency provided the data
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/university_houston/'
           'salaries/2015-05/Texas%20Tribune.csv')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    def process_hire_date(self, hire_date):
        # TODO five people don't have hire dates given
        year = hire_date[0:4]
        month = hire_date[4:6]
        day = hire_date[6:8]
        return "-".join([year, month, day])

    def calculate_tenure(self, hire_date):
        try:
            hire_date_data = map(int, hire_date.split('/'))
        except:
            return None
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            error_msg = ("An employee was hired after the data was provided.\n"
                         "Is DATE_PROVIDED correct?")
            raise ValueError(error_msg)
        return tenure

    @property
    def compensations(self):
        hire_date = self.process_hire_date(self.hire_date)
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                    'description': self.description
                },
                'tx_salaries.Employee': {
                    'hire_date': hire_date,
                    'compensation': self.compensation,
                    'tenure': self.calculate_tenure(hire_date),
                },
                'tx_salaries.EmployeeTitle': {
                    'name': unicode(
                        cleaver.DepartmentNameCleaver(self.job_title).parse())
                },
            }
        ]

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
