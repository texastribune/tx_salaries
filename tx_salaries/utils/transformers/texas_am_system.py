from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin, mixins.GenericDepartmentMixin,
        mixins.GenericIdentifierMixin, mixins.GenericJobTitleMixin,
        mixins.GenericPersonMixin, mixins.MembershipMixin,
        mixins.OrganizationMixin, mixins.PostMixin, mixins.RaceMixin,
        mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Worker Legal Name Last Name',
        'first_name': 'Worker Legal Name First Name',
        'middle_name': 'Worker Legal Name Middle Name',
        'department': 'Adloc Desc',
        'job_title': 'Title Description',
        'hire_date': 'Curr Empl Date',
        'compensation': 'Annual Budgeted Salary',
        'gender': 'Gender',
        'race': 'Race-Ethnicity',
        'organization_name': 'Mbr Name',
        'rate': 'Annual Term Mths',
        'full_or_part_time': 'Part/Full Time',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2018, 6, 22)

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'texas_a%26m_university_system/salaries/2018-06/tamu_system.xlsx')

    gender_map = {'Female': 'F', 'Male': 'M', 'Declined to Specify': 'Unknown'}

    @property
    def organization(self):
        return {
            'name': self.organization_name.strip(),
            'children': self.department_as_child,
            'classification': self.ORGANIZATION_CLASSIFICATION,
        }

    @property
    def description(self):
        rate = self.get_mapped_value('rate')
        rate = rate.rstrip('0').rstrip('.') if '.' in rate else rate
        return '{rate}-month salary'.format(rate=rate)

    @property
    def compensation_type(self):
        full_or_part_time = self.get_mapped_value('full_or_part_time')

        if full_or_part_time == 'F':
            return 'FT'

        return 'PT'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    def calculate_tenure(self):
            hire_date_data = map(int, self.hire_date.split('-'))
            hire_date = date(hire_date_data[0], hire_date_data[1],
                             hire_date_data[2])
            tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
            if tenure < 0:
                tenure = 0
            return tenure

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
