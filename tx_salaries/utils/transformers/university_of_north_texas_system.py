from . import base
from . import mixins

from datetime import date
from .. import cleaver


class TransformedRecord(
        mixins.GenericCompensationMixin, mixins.GenericDepartmentMixin,
        mixins.GenericIdentifierMixin, mixins.GenericJobTitleMixin,
        mixins.GenericPersonMixin, mixins.MembershipMixin,
        mixins.OrganizationMixin, mixins.PostMixin, mixins.RaceMixin,
        mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'NAME',
        # 'suffix': '', if needed
        'department': 'DEPTNAME',
        'job_title': 'JOBTITLE',
        'hire_date': 'HIRE_DATE',
        'compensation': 'TOTAL SALARY',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'status': 'FULL/PART TIME',
        'organization_name': 'COMPANY'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    # NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    # ORGANIZATION_NAME = 'The University of North Texas '
    organization_name_map = {
        'DAL': 'UNT Dallas',
        'HSC': 'UNT Health Science Center',
        'SYS': 'UNT System Administration',
        'UNT': 'University of North Texas'
    }

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # ???
    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Total salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2016, 6, 21)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'university_north_texas_system/salaries/'
           '2016-06/unt_system.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def organization_name(self):
        return self.organization_name_map[self.get_mapped_value(
            'organization_name').strip()]

    @property
    def organization(self):
        return {
            'name': self.organization_name,
            'children': self.department_as_child,
            'classification': self.ORGANIZATION_CLASSIFICATION,
        }

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            # 'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    @property
    def compensation_type(self):
        status = self.get_mapped_value('status')

        if float(status) >= 1:
            return 'FT'

        return 'PT'

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
