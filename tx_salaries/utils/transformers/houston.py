from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'middle_name': 'Mid Name',
        'department': 'Department Name',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'compensation': 'Gross Annual Salary',
        'gender': 'Gender',
        'race': 'Race',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Houston'

    ORGANIZATION_CLASSIFICATION = 'City'

    DATE_PROVIDED = date(2015, 10, 20)
    # Y/M/D agency provided the data

    URL = "http://raw.texastribune.org.s3.amazonaws.com/houston/salaries/2015-10/houston.xlsx"

    gender_map = {'Female': 'F', 'Male': 'M'}

    compensation_type = 'FT'
    description = 'Annualized base pay'

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
