from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'compensation_type': 'FT/PT',
        'race': 'Race',
        'gender': 'Gender',
        'compensation': 'Gross Annual Salary',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    gender_map = {'Female': 'F', 'Male': 'M'}

    ORGANIZATION_NAME = 'The University of Texas Health Science Center at San Antonio'

    # NEED EDITORIAL INPUT
    # compensation_type = 'Full Time'

    @property
    def is_valid(self):
        # TODO clarification needed on FT/PT
        if self.data['Gross Annual Salary'] == 'VARIES' or self.data['FT/PT'] == 'WOS':
            return False
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

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

#TODO needs custom identifier, people with multiple positions
transform = base.transform_factory(TransformedRecord)
