from . import base
from . import mixins

from datetime import date
from .. import cleaver


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'FNAME',
        'department': 'DEPT',
        'job_title': 'TITLE',
        'hire_date': 'HIREDATE',
        'compensation': 'GROSS',
        'employee_type': 'FULL_PART',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
    }

    ORGANIZATION_NAME = 'Midwestern State University'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2016, 5, 2)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'midwestern_state_university/salaries/2016-05/'
           'midwestern.xlsx')

    # There are some people listed as Other status, because they retired in 2015, which the data represents
    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.employee_type.strip() != 'O'

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('employee_type')

        if emptype == 'P':
            return 'PT'
        else:
            return 'FT'

    @property
    def description(self):
        emptype = self.get_mapped_value('employee_type')
        title = self.get_mapped_value('job_title')

        if emptype == 'P':
            return 'Part-time 2015 gross annual salary'

        if emptype == 'F':
            if title == 'President':
                return 'Budgeted annual salary'
            else:
                return '2015 gross annual salary'

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

    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()

transform = base.transform_factory(TransformedRecord)
