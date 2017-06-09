from . import base
from . import mixins

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'race': 'Race',
        'gender': 'Gender',
        'compensation': 'Annual Salary',
        'status': 'Full/Part',
    }

    ORGANIZATION_NAME = 'University of Texas at San Antonio'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2017, 6, 9)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/ut_san_antonio/'
            'salaries/2015-10/utsanantonio.xls')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

    @property
    def compensation_type(self):
        emp_type = self.status

        if emp_type == 'F':
            return 'FT'

        if emp_type == 'P':
            return 'PT'

    @property
    def description(self):
        emp_type = self.status

        if emp_type == 'F':
            return "Annual salary"

        if emp_type == 'P':
            return "Part-time annual salary"

    @property
    def race(self):
        if '2 or more' in self.get_mapped_value('race'):
            return {
                'name': 'Two or more races'
            }
        else:
            return {
                'name': self.get_mapped_value('race')
            }

    @property
    def person(self):
        name = self.get_name()
        gender = self.gender
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

    def get_raw_name(self):
        split_name = self.full_name.split(',')
        last_name = split_name[0]
        split_firstname = split_name[1].split(' ')
        first_name = split_firstname[0]
        if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
            middle_name = split_firstname[1]
        else:
            first_name = split_name[1]
            middle_name = ''

        return u' '.join([first_name, middle_name, last_name])


transform = base.transform_factory(TransformedRecord)
