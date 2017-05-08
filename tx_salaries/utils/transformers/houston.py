from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'middle_name': 'Mid Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'employee_type': 'Status',
        'wage_type': 'Base Pay Wage Type',
        'compensation': 'Base Pay Rate',
        'gender': 'Gender',
        'race': 'Race',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Houston'

    ORGANIZATION_CLASSIFICATION = 'City'

    DATE_PROVIDED = date(2017, 5, 3)

    URL = "http://raw.texastribune.org.s3.amazonaws.com/houston/salaries/2017-05/houston.xlsx"

    gender_map = {'Female': 'F', 'Male': 'M'}

    department_map = {
        '1000': 'Houston Police',
        '1100': 'Neighborhood',
        '1200': 'Houston Fire',
        '1500': 'Houston Emergency Center',
        '1600': 'Municipal Court',
        '2000': 'Public Works & Engineering',
        '2100': 'Solid Waste',
        '2500': 'General Service',
        '2800': 'Houston Airport System',
        '3200': 'Housing & Community Development',
        '3400': 'Houston Public Library',
        '3600': 'Parks & Recreation',
        '3800': 'Health & Human Services',
        '4200': 'Convention',
        '5000': 'Mayors Office',
        '5100': 'Office of Business Opportunity',
        '5500': 'City Council',
        '6000': 'Controllers',
        '6400': 'Finance',
        '6500': 'Admin. & Regulatory Affairs',
        '6700': 'Fleet',
        '6800': 'Houston IT Services',
        '7000': 'Planning',
        '7500': 'City Secretary',
        '8000': 'Human Resources',
        '9000': 'Legal',
    }

    @property
    def is_valid(self):
        return self.last_name.strip() != ''

    @property
    def compensation(self):
        pay = self.get_mapped_value('compensation')
        status = self.get_mapped_value('employee_type')
        wage_type = self.get_mapped_value('wage_type')

        if status == 'Full Time':
            if wage_type == 'Cadet Period Salary':
                # cadets salary is listed outright
                return pay
            else:
                # everyone else is two-week period, multiple by 26 for annual
                return pay * 26
        else:
            # part-timers are listed for 80 hours like full-timers, but we can't
            # say how many hours they work, so can't multiply. Instead, I divide
            # by 80 and just list their hourly rate
            return pay / 80


    @property
    def compensation_type(self):
        status = self.get_mapped_value('employee_type')
        wage_type = self.get_mapped_value('wage_type')

        # cadets are listed as full-timers but we dont want them in the calcs
        if status == 'Full Time' && wage_type != 'Cadet Period Salary':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        status = self.get_mapped_value('employment_type')
        wage_type = self.get_mapped_value('wage_type')

        if status == 'Full Time':
            if wage_type == 'Cadet Period Salary':
                return 'Cadet Period Salary'
            else:
                return 'Annualized base pay'
        else:
            'Part-time hourly rate'

    @property
    def department(self):
        return self.department_map[self.department.strip()]


    @property
    def race(self):
        if self.race == '':
            return {
                'name': 'Not specified'
            }
        else:
            return {
                'name': self.race.strip()
            }

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

transform = base.transform_factory(TransformedRecord)
