from datetime import date

from . import base
from . import mixins

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'NAME LAST',
        'first_name': 'NAME FIRST',
        'middle_name': 'NAME MIDDLE',
        'suffix_name': 'NAME SUFFIX',
        'department': 'DEPARTMENT',
        'job_title': 'TITLE',
        'hire_date': 'CONTINUOUS EMPLOYMENT DATE',
        'employee_type': 'EMPLOYMENT TYPE',
        'gender': 'GENDER',
        'given_race': 'RACE',
        'compensation': 'SALARY (FY ALLOCATION)',
    }

    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at Austin'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2015, 6, 29)

    URL = 'http://s3.amazonaws.com/raw.texastribune.org/ut_austin/salaries/2015-06/ut_austin.xlsx'

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
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'FULL TIME':
            return 'FT'

        if employee_type == 'PART TIME':
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'FULL TIME':
            return "Annual salary"

        if employee_type == 'PART TIME':
            return "Part-time annual salary"

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()],
        }
        print r
        return r

    def calculate_tenure(self, hire_date):
        try:
            hire_date_data = map(int, hire_date.split('-'))
        except:
            return None
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        # if tenure < 0:
        #     error_msg = ("An employee was hired after the data was provided.\n"
        #                  "Is DATE_PROVIDED correct?")
        #     raise ValueError(error_msg)
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
                    'name': self.job_title,
                },
            }
        ]

    @property
    def race(self):
        race = self.given_race.strip()
        if race == '':
            race = 'Not given'
        return {'name': race}

transform = base.transform_factory(TransformedRecord)
