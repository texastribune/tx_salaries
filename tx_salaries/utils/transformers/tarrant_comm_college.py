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
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'status': 'FT/PT',
        # 'contract': 'Months of Contract',
        'gender': 'Gender',
        'given_race': 'Race/Ethnicity',
        'compensation': 'Salary (FT Annual ) (PT  Hourly)',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Tarrant County College'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    DATE_PROVIDED = date(2017, 11, 10)

    URL = ('http://s3.amazonaws.com/raw.texastribune.org/tarrant_county_college/'
        'salaries/2015-11/tarrantcountycollege.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('status')

        if emptype == 'FT':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        status = self.get_mapped_value('status')

        if status == 'PT':
            return 'Hourly rate'
        elif status == 'FT':
            return 'Annual salary'

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

transform = base.transform_factory(TransformedRecord)
