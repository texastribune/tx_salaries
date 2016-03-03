from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Start Date',
        'compensation': ' Annual Rt ',
        'gender': 'Sex',
        'race': 'Race',
        'employee_type':  'Full/Part',
    }

    ORGANIZATION_NAME = 'University of Texas of the Permian Basin'

    ORGANIZATION_CLASSIFICATION = 'Universtiy'

    description = 'Annual rate'

    DATE_PROVIDED = date(2016, 2, 29)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/ut_permian_basin'
           '/salaries/2016-02/ut_permbasin.xls')

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

    def get_raw_name(self):
        split_name = self.full_name.split(', ')

        return u' '.join([split_name[1], split_name[0]])


transform = base.transform_factory(TransformedRecord)
