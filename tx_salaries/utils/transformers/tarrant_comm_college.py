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
        'gender': 'Gender',
        'race': 'Race/Ethnicity',
        'compensation': 'Salary (FT Annual ) (PT  Hourly)',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Tarrant County College'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    DATE_PROVIDED = date(2017, 11, 13)

    # UPDATE THIS URL WITH 2017 URL WHEN CLEAN DATA COMES BACK
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'tarrant_county_college/salaries/2017-12/'
           'tarrant-county-college.xlsx')

    @property
    def is_valid(self):
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
        status = self.status

        if status == 'PT':
            return 'Hourly rate'
        else:
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
