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
        'department': 'Department Title',
        'job_title': 'Assignment Title',
        'employee_type': 'Full Part Time',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Salary',
        'gender': 'Sex',
        'white': 'White',
        'black': 'Black or African American',
        'asian': 'Asian',
        'native': 'American Indian or Alaskan Native',
        'hawaiian': 'Hawaiian Pacific Islander',
        'hispanic': 'Of Hispanic or Latino Descent',
    }

    hispanic_map = {'Yes': 'Hispanic', '': 'Non-Hispanic'}

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Bryan ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    DATE_PROVIDED = date(2016, 6, 9)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'bryan_isd/salaries/2016-06/bryan-isd.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.get_mapped_value('employee_type')

        if employee_type == 'F':
            return "FT"

        if employee_type == 'P':
            return "PT"

        return "FT"

    @property
    def description(self):
        employee_type = self.get_mapped_value('employee_type')

        if employee_type == 'F':
            return "Annual Salary"

        if employee_type == 'P':
            return "Part-time annual salary"

        return "Annual Salary"

    @property
    def race(self):
        races = [self.get_mapped_value('white'),self.get_mapped_value('black'),
        self.get_mapped_value('asian'),self.get_mapped_value('native'),
        self.get_mapped_value('hawaiian')]
        raceNames = ['White','Black or African American','Asian',
        'American Indian or Alaskan Native','Hawaiian Pacific Islander']
        ethnicity = self.hispanic_map[self.hispanic.strip()]

        i = 0
        raceList = []

        for indivRace in races:
            if indivRace == 'X':
                raceList.append(raceNames[i])
            i += 1

        if len(raceList) > 1:
            return {
                'name': 'Two or more races, ' + ethnicity
            }
        elif len(raceList) == 0:
            return {
                'name': 'Not given'
            }
        else:
            return {
                'name': raceList[0] + ', ' + ethnicity
            }

    @property
    def person(self):
        name = self.get_name()

        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            return 0
        return tenure


transform = base.transform_factory(TransformedRecord)
