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
        'full_name': 'Employee Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Date of Hire',
        'employee_type': 'Full or Part Time',
        'gender': 'Gender',
        'given_race': 'Race',
        'compensation': 'Salary',
    }

    gender_map = {u'Female': u'F', u'Male': u'M'}

    ORGANIZATION_NAME = 'Texas Tech University Health Sciences Center'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2016, 03, 24)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'texas_tech_health_science/salaries/2016-03/ttuhsc.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return 'FT'

        if employee_type == 'P':
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return "Salary"

        if employee_type == 'P':
            return "Part-time salary"

    @property
    def race(self):
        return {
            'name': self.get_mapped_value('given_race').strip()
        }

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.get_mapped_value('gender')],
        }

        return r

    def get_raw_name(self):
        split_name = self.full_name.split(', ')
        last_name = split_name[0]
        split_firstname = split_name[1].split(' ')
        first_name = split_firstname[0]
        if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
            middle_name = split_firstname[1]
        else:
            first_name = split_name[1]
            middle_name = ''

        return u' '.join([first_name, middle_name, last_name])

    @property
    def organization(self):
        return {
            'name': self.ORGANIZATION_NAME,
            'classification': self.ORGANIZATION_CLASSIFICATION,
            'children': self.department_as_child,
        }

    @property
    def department_as_child(self):
        fullDept = self.department

        if ' Ama ' in fullDept or fullDept.endswith(' Ama'):
            fullDept = fullDept.replace(' Ama', ' Amarillo')
        if ' Lbk ' in fullDept or fullDept.endswith(' Lbk'):
            fullDept = fullDept.replace(' Lbk', ' Lubbock')
        if ' Elp ' in fullDept or fullDept.endswith(' Elp'):
            fullDept = fullDept.replace(' Elp', ' El Paso')
        if ' Ode ' in fullDept or fullDept.endswith(' Ode'):
            fullDept = fullDept.replace(' Ode', ' Odessa')
        if ' Abi ' in fullDept or fullDept.endswith(' Abi'):
            fullDept = fullDept.replace(' Abi', ' Abilene')
        if ' Dal ' in fullDept or fullDept.endswith(' Dal'):
            fullDept = fullDept.replace(' Dal', ' Dallas')

        return [{'name': unicode(fullDept), }, ]

transform = base.transform_factory(TransformedRecord)
