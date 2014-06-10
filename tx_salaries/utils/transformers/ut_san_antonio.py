from datetime import date

from . import base
from . import mixins

# http://raw.texastribune.org.s3.amazonaws.com/ut_san_antonio/salaries/2014-01/Hill1931-responsive.xls


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'race': 'Ethnicity',
        'gender': 'Sex',
        'compensation': 'Annual Salary',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    gender_map = {'Female': 'F', 'Male': 'M'}

    ORGANIZATION_NAME = 'University of Texas at San Antonio'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO 45 earn < 10,000
    compensation_type = 'Full Time'

    DATE_PROVIDED = date(2014, 1, 21)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != '' or self.hire_date.strip() != ''

    @property
    def person(self):
        data = {
            'family_name': self.last_name,
            'given_name': self.first_name,
            'name': self.get_raw_name(),
        }
        try:
            data.update({
                'gender': self.gender_map[self.gender.strip()]
            })
            return data
        except KeyError:
            return data


transform = base.transform_factory(TransformedRecord)
