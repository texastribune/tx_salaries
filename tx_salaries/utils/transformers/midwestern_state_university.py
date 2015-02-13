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
        'last_name': 'LAST_NAME',
        'first_name': 'FIRST_NAME',
        'middle_name': 'MI',
        'suffix': 'SUFFIX',
        'department': 'DEPT',
        'job_title': 'TITLE',
        'hire_date': 'CURR_HIRE',
        'compensation': 'ANN_SAL',
        'gender': 'GENDER',
        'race': 'RACE',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', 'suffix', )

    ORGANIZATION_NAME = 'Midwestern State University'

    ORGANIZATION_CLASSIFICATION = 'University'

    compensation_type = 'FT'

    description = 'Annual salary'

    DATE_PROVIDED = date(2015, 2, 12)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'midwestern_state_university/salaries/2015-02/'
           'midwestern_state_university.xlsx')

    gender_map = {'Female': 'F', 'Male': 'M'}

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

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
