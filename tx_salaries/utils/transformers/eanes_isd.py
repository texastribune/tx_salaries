from datetime import date

from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Name - Last Name',
        'middle_name': 'Name - Middle Name',
        'first_name': 'Name - First Name',
        'department': 'Department',
        'job_title': 'Emp Type Code',
        'hire_date': 'Hire Date',
        'compensation': 'Actual Calc\' Contract Pay',
        'race': 'Race Desc',
        'gender': 'Gender',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Eanes ISD'
    ORGANIZATION_CLASSIFICATION = 'School District'

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/eanes_isd/salaries/2013-08/TPIA%20NO.3812.xls'

    DATE_PROVIDED = date(2014, 3, 10)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        return 'Full Time'

    @property
    def compensation(self):
        raw = self.get_mapped_value('compensation')
        return raw.strip(' $').replace(',', '')

    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('/'))
        hire_date = date(hire_date_data[2], hire_date_data[0],
                         hire_date_data[1])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            error_msg = ("An employee was hired after the data was provided.\n"
                         "Is DATE_PROVIDED correct?")
            raise ValueError(error_msg)
        return tenure

transform = base.transform_factory(TransformedRecord)
