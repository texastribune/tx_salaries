from datetime import date

from . import base
from . import mixins

from .. import cleaver

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

    cleaver.DepartmentName.MAP = (cleaver.DepartmentName.MAP +
                                 ((cleaver.regex_i(r'vp '), 'Vice President '), ) +
                                 ((cleaver.regex_i(r'^Its '), 'ITS '), ) +
                                 ((cleaver.regex_i(r'^Kut '), 'KUT '), ) +
                                 ((cleaver.regex_i(r'^Phr '), 'PHR '), ) +
                                 ((cleaver.regex_i(r'^Fs '), 'FS '), ) +
                                 ((cleaver.regex_i(r'^Dns '), 'DNS '), ) +
                                 ((cleaver.regex_i(r'^Pmcs '), 'PMCS '), ) +
                                 ((cleaver.regex_i(r'^Bfs '), 'BFS '), ) +
                                 ((cleaver.regex_i(r'Aces - It '), 'ACES - IT '), ) +
                                 ((cleaver.regex_i(r'Uteach'), 'UTeach'), ))

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

        return 'FT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'FULL TIME':
            return "Annual salary"

        if employee_type == 'PART TIME':
            return "Part-time annual salary"

        return "Annual salary"

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
        }
        if self.is_mapped_value('gender'):
            gender = self.get_mapped_value('gender')
            if gender.split() == '':
                gender = 'Not given'
            r['gender'] = gender

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
    def post(self):
        return {'label': (unicode(cleaver.DepartmentNameCleaver(self.job_title)
                                         .parse()))}

    @property
    def race(self):
        race = self.given_race.strip()
        if race == '':
            race = 'Not given'
        return {'name': race}

    @property
    def department_as_child(self):
        return [{'name': unicode(cleaver.DepartmentNameCleaver(self.department)
                                        .parse()), }, ]

transform = base.transform_factory(TransformedRecord)
