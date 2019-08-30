from . import base
from . import mixins
from .. import cleaver
from datetime import date

import string

class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Salary Rate',
        'gender': 'Gender',
        'given_race': 'RaceEthinicity',
        'employee_type': 'Fulltime or Parttime',
    }

    ORGANIZATION_NAME = 'University of Texas at Austin'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2019, 9, 5)

    URL = "http://raw.texastribune.org.s3.amazonaws.com/ut_austin/salaries/2019-07/employee_data_new.xlsx"

    gender_map = {
        'Female':'F',
        'Male':'M',
        '': 'Unknown'
    }

    description = 'Annual salary rate'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

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

    @property
    def job_title(self):
        title = self.get_mapped_value('job_title').split(' - ')[1]

        return title

    @property
    def race(self):
        race = self.given_race.strip()

        return {'name': race}

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'Full-time':
            return 'FT'

        if employee_type == 'Part-time':
            return 'PT'


    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()

transform = base.transform_factory(TransformedRecord)
