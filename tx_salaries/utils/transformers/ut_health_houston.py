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
        'job_title': 'Job Title',
        'department': 'Department',
        'race': 'Ethnicity - Consolidated',
        'gender': 'Gender',
        'compensation_type': 'Employment Status',
        'hire_date': 'Original Hire Date',
        'compensation': 'Total Base Comp',
    }

    # COMPENSATION_MAP = {
    #     'FT': 'F',
    #     'PT': 'P'
    # }

    RACE_MAP = {
        'WHITE': 'White',
        'ASIAN': 'Asian',
        'HISPA': 'Hispanic',
        'NSPEC': 'Not specified',
        'BLACK': 'Black',
        'Two or more races': 'Two or more races',
        'AMIND': 'American Indian',
        'PACIF': 'Pacific Islander',
        'not available': 'Not specified',
    }

    # gender_map = {'F': 'F', 'M': 'M'}

    description = 'Total compensation rate'

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = (
        'The University of Texas Health Science Center at Houston')

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2018, 5, 9)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    URL = (
        'https://s3.amazonaws.com/raw.texastribune.org/ut_health_houston/'
        'salaries/2016-10/ut-health-science-houston-10-14-16.xlsx')

    # @property
    # def compensation_type(self):
    #     return self.COMPENSATION_MAP[
    #         self.get_mapped_value('compensation_type')]

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
    def compensation_type(self):
        status = self.get_mapped_value('compensation_type')

        if status == 'F':
            return 'FT'
        elif status == 'P':
            return 'PT'

    @property
    def description(self):
        status = self.get_mapped_value('compensation_type')

        if status == 'F':
            return 'Base compensation rate'
        elif status == 'P':
            return 'Part-time base compensation rate'

    # @property
    # def description(self):
    #     compensation_type = self.compensation_type

    #     if compensation_type == 'F':
    #         return 'Base compensation rate'

    #     if compensation_type == 'P':
    #         return 'Part-time base compensation rate'


transform = base.transform_factory(TransformedRecord)
