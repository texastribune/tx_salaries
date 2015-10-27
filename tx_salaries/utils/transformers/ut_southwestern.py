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
        'race': 'Race',
        'compensation': 'Gross Annual Salary',
    }

    gender_map = {'Female': 'F', 'Male': 'M', '': 'Unknown'}

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'UT Southwestern Medical Center'

    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2015, 8, 31)

    URL = ('http://s3.amazonaws.com/raw.texastribune.org/ut_southwestern_medical'
        '/salaries/2015-08/ut_southwestern.xlsx')



    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.compensation.strip() != '0'


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

        if employee_type == 'Full-Time':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type
        pay_rate = self.compensation.strip()

        if employee_type == 'Full-Time':
            return 'Gross annual salary'

        if employee_type == 'Part-Time':
            #weird ones that were hourly
            if pay_rate == '10.4' or pay_rate == '9.75' or pay_rate == '8':
                return 'Part-time hourly rate'
            else:
                return 'Part-time annual salary'

        if employee_type == 'PRN':
            return 'Part-time "as needed" annual salary'

        if employee_type == 'WIP':
            return 'Part-time Weekend Incentive Program salary'

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

transform = base.transform_factory(TransformedRecord)
