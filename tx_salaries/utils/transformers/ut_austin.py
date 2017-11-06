from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericIdentifierMixin,
    mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'NAME LAST',
        'first_name': 'NAME FIRST',
        'middle_name': 'NAME MIDDLE',
        'suffix_name': 'NAME SUFFIX',
        'department': 'DEPARTMENT',
        'job_title': 'TITLE',
        'hire_date': 'HIRE DATE',
        'employee_type': 'EMPLOYMENT TYPE',
        'gender': 'GENDER',
        'given_race': 'RACE',
        'compensation': 'SALARY (FISCAL YEAR ALLOCATION)',
    }

    gender_map = {
        'FEMALE':'F',
        'MALE':'M',
        '': 'Unknown'
    }

    ORGANIZATION_NAME = 'University of Texas at Austin'
    ORGANIZATION_CLASSIFICATION = 'University'
    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    DATE_PROVIDED = date(2017, 7, 6)


    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
    'ut_austin/salaries/2017-07/OPENRECORDS.ESSIG.20160705.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.gender.strip() != ''

    @property
    def department(self):
        department = self.get_mapped_value('department').title()

        return department

    @property
    def race(self):
        race = self.given_race.strip().title()

        if race == '':
            race = 'Unknown'
        return {
            'name': race
        }

    @property
    def gender(self):
        sex = self.gender_map[self.get_mapped_value('gender')].strip().title()

        if sex == "":
            return ""
        return sex

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender,
        }

        return r

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
            return "Fiscal year allocation"

        if employee_type == 'PART TIME':
            return "Part-time compensation"

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

transform = base.transform_factory(TransformedRecord)
