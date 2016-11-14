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
    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'id_number': 'ID',
        'job_title': 'Job Title',
        'department': 'Dept',
        'race': 'Ethnic Grp',
        'gender': 'Sex',
        'compensation_type': 'Full/Part',
        'hire_date': 'Start Date',
        'compensation': 'Total Comp Rate',
    }

    COMPENSATION_MAP = {
        'F': 'FT',
        'P': 'PT'
    }

    description = 'Total compensation rate'

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = (
        'The University of Texas Health Science Center at Houston')

    # TODO current app uses University Hospital
    ORGANIZATION_CLASSIFICATION = 'University Hospital'

    DATE_PROVIDED = date(2015, 8, 10)

    is_valid = True

    URL = (
        'https://s3.amazonaws.com/raw.texastribune.org/ut_health_houston/'
        'salaries/2016-10/ut-health-science-houston-10-14-16.xlsx')

    @property
    def compensation_type(self):
        return self.COMPENSATION_MAP[
            self.get_mapped_value('compensation_type')]

transform = base.transform_factory(TransformedRecord)
