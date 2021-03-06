from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last name',
        'first_name': 'First name',
        # 'middle_name': '', if needed
        # 'full_name': '', if needed
        # 'suffix': '', if needed
        'department': 'Dept.',
        'job_title': 'Title',
        'hire_date': 'ORIG HD',
        'compensation': 'Annual salary',
        'gender': 'Gender Key',
        'race': 'Ethnic origin',
        'status': 'PT/FT'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Metropolitan Transit Authority'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'Transit'

    # `compensation_type` determines what type of salary this is, and is taken into account when calculating
    # stats. The only two valid options are `FT` and `PT`
    compensation_type = 'FT'

    # How would you describe the compensation field? We try to respect how they use their system.
    description = 'Annual salary'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 2, 20)

    # The URL to find the raw data in our S3 bucket.
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'metropolitan_transit_authority/salaries/2017-02/'
           'metropolitan_transit_authority.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'Female': 'F', 'Male': 'M'}

    description_map = {
        'FT Hrly NE Maint': 'Full Time Hourly Non Exempt Maintenance',
        'FT Hrly NE PSA': 'Full Time Hourly- Professional Services Agreement (temporary)',
        'FT Hrly NE Transp': 'Full Time Hourly Non Exempt Transportation',
        'FT Salaried Exempt': 'Full Time Salaried Exempt',
        'FT Salaried NE': 'Full Time Salaried Non Exempt',
        'PT Hrly NE Non Union': 'Part Time Hourly Non Exempt Non-Union',
        'PT Hrly NE Ret-Maint': 'Part Time Hourly Non Exempt Retired-Maintenance',
        'PT Hrly NE Ret-Trans': 'Part Time Non Exempt Retired-Transportation',
        'PT Hrly NE Transp': 'Part Time Hourly Non Exempt Transportation'
    }

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    def process_compensation_description(self):
        return self.description_map[self.compensation_type.strip()].title()

    @property
    def description(self):
        compDescription = self.description_map[self.status.strip()].title()
        return compDescription

    @property
    def compensation_type(self):
        status = self.status
        # checks full-time/part-time status and labels accordingly
        if 'FT' in status:
            return 'FT'
        elif 'PT' in status:
            return 'PT'

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

transform = base.transform_factory(TransformedRecord)
