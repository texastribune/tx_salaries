from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Full Name',
        'department': 'Building Code Desc',
        'job_title': 'Position Group Desc',
        'hire_date': 'Hire Date',
        'compensation': 'Position Contract Amt',
        'gender': 'Gender',
        'race': 'Race Desc',
    }

    ORGANIZATION_NAME = 'Allen ISD'

    ORGANIZATION_CLASSIFICATION = 'School District'

    compensation_type = 'FT'

    description = 'Position contract amount'

    DATE_PROVIDED = date(2014, 12, 15)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/allen_isd'
           '/salaries/2014-12/TexasTribuneDec2014.xls')

    gender_map = {'Female': 'F', 'Male': 'M'}

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def hire_date(self):
        raw_date = self.get_mapped_value('hire_date')
        return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

    @property
    def compensation(self):
        return self.get_mapped_value('compensation').replace(',', '')

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
        last_name = split_name[0]
        split_firstname = split_name[1].split(' ')
        first_name = split_firstname[0]
        if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
            middle_name = split_firstname[1]
        else:
            first_name = split_name[1]
            middle_name = ''

        return u' '.join([first_name, middle_name, last_name])


transform = base.transform_factory(TransformedRecord)
