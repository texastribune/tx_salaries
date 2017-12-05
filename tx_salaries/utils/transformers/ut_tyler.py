from datetime import date

from . import base
from . import mixins


class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'last_name': 'Last',
        'first_name': 'First',
        'department': 'Dept Descr',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'status': 'Full Time/Part Time Status',
        'gender': 'Gender',
        'nationality': 'Race',
        'compensation': 'Gross Annual Salary',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'UT Tyler'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2017, 11, 14)

    race_map = {
        'AMIND': 'American Indian',
        'ASIAN': 'Asian',
        'BLACK': 'Black',
        'HISPA': 'Hispanic',
        'NSPEC': 'Not Specified',
        'WHITE': 'White',
        'PACIF': 'Pacific Islander',
        'No Record': 'Not Specified'
    }

    URL = ('http://s3.amazonaws.com/raw.texastribune.org/tarrant_county_college/'
           'salaries/2015-11/tarrantcountycollege.xlsx')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('status')

        if emptype == 'Full Time' or emptype == 'FA3':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        status = self.status

        if status == 'Part-Time':
            return 'Part-time salary'
        else:
            return 'Gross annual salary'

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

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }


transform = base.transform_factory(TransformedRecord)
