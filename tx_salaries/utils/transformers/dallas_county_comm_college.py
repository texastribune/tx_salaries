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
        'last_name': 'Last Name ',
        'first_name': 'First Name ',
        'middle_name': 'Middle Name ',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Latest Hire Date',
        'gender': 'Gender',
        'given_race': 'Ethnicity/Race',
        'employee_type': 'Emp Type',
        'compensation': 'Annual Salary',
        'rate': 'Hrly Rate',
    }

    gender_map = {u'Female': u'F', u'Male': u'M'}

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Dallas County Community College District'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    DATE_PROVIDED = date(2016, 2, 17)

    URL = 'http://s3.amazonaws.com/raw.texastribune.org/dallas_county_community_college_district/salaries/2016-02/dcccd.xlsx'

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

    @property
    def gender(self):
        sex = self.gender_map[self.get_mapped_value('gender')]
        if sex.strip() == "":
            return ""
        return sex.strip()

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
