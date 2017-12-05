from . import base
from . import mixins

import string

from datetime import date

class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericIdentifierMixin,
    mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'FULL_NAME',
        'department_name': 'ORGANIZATION',
        'job_title': 'TITLE',
        'hire_date': 'Hire Date',
        'compensation': 'Salary',
        'gender': 'Gender',
        'race': 'ETHNICITY',
        'status': 'Full time/Part time'
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'Dallas ISD'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 6, 22)

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas_isd/salaries/2017-05/orr16243-rev2.xlsx')

    # This is how the loader checks for valid people. Defaults to checking to
    # see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    # @property
    # def hire_date(self):
    #     raw_date = self.get_mapped_value('hire_date')
    #     return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

    @property
    def compensation_type(self):
        emp_type = self.status

        if emp_type == 'Full-Time':
            return 'FT'

        if emp_type == 'Part-Time':
            return 'PT'

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

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

    @property
    def description(self):
        return 'Salary'


    @property
    def job_title(self):
        # don't title case roman numerals
        title = self.get_mapped_value('job_title')
        split = title.split('II')
        split_two = title.split('IV')
        split_three = title.split(' V')

        if len(split) == 1 and len(split_two) == 1 and len(split_three) == 1:
            return title.title()
        elif len(split) > 1:
            return split[0].title() + ' II' + split[1]
        elif len(split_two) > 1:
            return split_two[0].title() + ' IV'
        elif len(split_three) > 1:
            return split_three[0].title() + ' V'

    @property
    def department(self):
        # don't title case roman numerals
        dept = self.get_mapped_value('department_name').title()
        split = dept.split('Eha')
        split_two = dept.split("'S")
        split_three = dept.split("Hs")
        split_four = dept.split("Vi-B")
        split_five = dept.split("It-")

        if len(split) == 1 and len(split_two) == 1 and len(split_three) == 1 and len(split_four) == 1 and len(split_five) == 1:
            return dept
        elif len(split) > 1:
            return dept.replace("Eha","EHA")
        elif len(split_two) > 1:
            return dept.replace("'S","'s")
        elif len(split_three) > 1:
            return dept.replace("Hs","HS")
        elif len(split_four) > 1:
            return dept.replace("Vi-B","VI-B")
        elif len(split_five) > 1:
            return dept.replace("It-","IT-")

    # def get_raw_name(self):
    #     split_name = self.full_name.split(', ')
    #     last_name = split_name[0]
    #     split_firstname = split_name[1].split(' ')
    #     first_name = split_firstname[0]
    #     if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
    #         middle_name = split_firstname[1]
    #     else:
    #         first_name = split_name[1]
    #         middle_name = ''

    #     return u' '.join([first_name, middle_name, last_name])

transform = base.transform_factory(TransformedRecord)
