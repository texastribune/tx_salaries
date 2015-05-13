from . import base
from . import mixins

from datetime import date

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Job Descr',
        'hire_date': 'Start Date',
        'compensation': 'Annual Rt',
        'gender': 'Sex',
        'race': 'Ethnic Grp',
    }

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'University of Houston'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    compensation_type = 'FT'

    description = 'Annual salary'

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    DATE_PROVIDED = date(2015, 4, 30)
    # Y/M/D agency provided the data
    URL = 'http://raw.texastribune.org.s3.amazonaws.com/university_houston/salaries/2015-05/Texas%20Tribune.csv'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def hire_date(self):
        return self.get_mapped_value('hire_date').split('T')[0]

    # def get_raw_name(self):
    #     middle_name_field = self.middle_name.strip()

    #     if middle_name_field == '' or middle_name_field == '(null)':
    #         self.NAME_FIELDS = ('first_name', 'last_name', )

    #     name_fields = [getattr(self, a).strip() for a in self.NAME_FIELDS]
    #     return u' '.join(name_fields)

    def get_raw_name(self):
        split_name = self.full_name.split(',')
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
