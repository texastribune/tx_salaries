from . import base
from . import mixins

from datetime import date

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LNAME',
        'first_name': 'FNAME',
        'department': 'DEPT',
        'job_title': 'TITLE',
        'hire_date': 'HIREDATE',
        'compensation': 'BUDGETED_SALARY',
        'gender': 'SEX',
        'race': 'Race',
        'employee_type': 'Status'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Beaumont ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    compensation_type = 'FT'

    description = 'Budgeted salary'

    DATE_PROVIDED = date(2016, 2, 26)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/beaumont_isd/salaries/2016-02/beaumontisd.xlsx'

    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False
    #Contract and Part-time employees just list their salary as 'hourly' or 'contract'

    @property
    def is_valid(self):
        return self.employee_type.strip() == 'Full Time'


    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
            'gender': self.gender,
        }

        return r

transform = base.transform_factory(TransformedRecord)
