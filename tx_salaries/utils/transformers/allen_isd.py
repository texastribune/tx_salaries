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
        'full_name': 'Full Name',
        'department': 'Building Code Desc',
        'job_title': 'Position Group Desc',
        'hire_date': 'Hire Date',
        'compensation': 'Position Contract Amt',
        'gender': 'Gender',
        'race': 'Race Desc',
        'employee_type': 'Position Job Type Desc',
    }

    ORGANIZATION_NAME = 'Allen ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    compensation_type = 'FT'

    description = 'Position contract amount'

    DATE_PROVIDED = date(2016, 4, 6)

    URL = ('https://raw.texastribune.org.s3.amazonaws.com/'
           'allen_isd/salaries/2016-04/allen-isd.xlsx')

    gender_map = {'Female': 'F', 'Male': 'M'}
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def hire_date(self):
        raw_date = self.get_mapped_value('hire_date')
        return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

    @property
    def compensation(self):
        return self.get_mapped_value('compensation').replace(',', '')

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type.endswith('P'):
            return 'PT'
        elif employee_type == '':
            return 'FT'
        else:
            return 'FT'

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

    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()


transform = base.transform_factory(TransformedRecord)
