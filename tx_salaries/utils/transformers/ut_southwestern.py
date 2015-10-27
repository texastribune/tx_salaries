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
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'middle_name': 'Middle Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'employee_type': 'Employment Type',
        'gender': 'Gender',
        'given_race': 'Race',
        'compensation': ' Gross Annual Salary ',
    }

    gender_map = {'Female': 'F', 'Male': 'M', '': 'Unknown'}

    ORGANIZATION_NAME = 'UT Southwestern Medical Center'

    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2015, 8, 31)

    URL = ('http://s3.amazonaws.com/raw.texastribune.org/ut_southwestern_medical'
        '/salaries/2015-08/ut_southwestern.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def hire_date(self):
        hire_date = self.get_mapped_value('hire_date')
        if hire_date.strip() == "":
            return ""
        year = hire_date[0:4]
        month = hire_date[4:6]
        day = hire_date[6:8]
        return "-".join([year, month, day])

    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            tenure = 0
        return tenure

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
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()],
        }

        return r

    @property
    def race(self):
        race = self.given_race.strip()
        if race == '':
            race = 'UNKNOWN'
        return {'name': race}


    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            tenure = 0
        return tenure

transform = base.transform_factory(TransformedRecord)
