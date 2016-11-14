from datetime import date

from . import base
from . import mixins


class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin,
    mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
    mixins.GenericJobTitleMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    # They included people without compensation and have
    # clarified they do not consider them employees
    # REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'id_number': 'ID',
        'job_title': 'Job Title',
        'department': 'Department',
        'race': 'Ethnicity',
        'gender': 'Gender',
        'compensation_type': 'Employment Status',
        'hire_date': 'Original Hire Date',
        'compensation': 'Total Base Comp',
    }

    COMPENSATION_MAP = {
        'F': 'FT',
        'P': 'PT'
    }

    RACE_MAP = {
        'WHITE': 'White',
        'ASIAN': 'Asian',
        'HISPA': 'Hispanic',
        'NSPEC': 'Not specified',
        'BLACK': 'Black',
        'TWO OR MORE': 'Two or more races',
        'AMIND': 'American Indian',
        'PACIF': 'Pacific Islander',
    }

    description = 'Total compensation rate'

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = (
        'The University of Texas Health Science Center at Houston')

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2016, 10, 14)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    URL = (
        'https://s3.amazonaws.com/raw.texastribune.org/ut_health_houston/'
        'salaries/2016-10/ut-health-science-houston-10-14-16.xlsx')

    @property
    def compensation_type(self):
        return self.COMPENSATION_MAP[
            self.get_mapped_value('compensation_type')]

    @property
    def race(self):
        raw_race = self.get_mapped_value('race')

        if raw_race == '':
            converted_race = 'Not specified'
        else:
            converted_race = self.RACE_MAP[raw_race]

        return {
            'name': converted_race
        }

    @property
    def description(self):
        compensation_type = self.compensation_type

        if compensation_type == 'FT':
            return 'Base compensation rate'

        if compensation_type == 'PT':
            return 'Part-time base compensation rate'


transform = base.transform_factory(TransformedRecord)
