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
        'last_name': 'LAST NAME',
        'first_name': 'FIRST NAME',
        'department': 'BUSINESS AREA',
        'job_title': 'JOB TITLE',
        'hire_date': 'HIRE DATE1',
        'compensation': 'FY16 ANNUAL SALARY2',
        'gender': 'GENDER',
        'nationality': 'ETHNIC ORIGIN10',
        'employee_type': 'EMPLOYEE SUBGROUP',
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'San Antonio'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'City'

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 6, 23)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'san_antonio/salaries/2017-06/'
           'W156567-020817_FY16.xlsx')

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    # This is how the loader checks for valid people. Defaults to checking to see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.
        if self.employee_type.strip() == 'TEMP':
            return False
        return True

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
    def compensation_type(self):
        employee_type = self.employee_type.upper()
        split = employee_type.split("PART-TIME")
        split_two = employee_type.split(" PT")
        split_three = employee_type.split("SCHOOL X'ING GUAR")

        if len(split) > 1 or len(split_two) > 1 or len(split_three) > 1:
            return 'PT'
        return 'FT'

    @property
    def description(self):
        employee_type = self.employee_type
        split = employee_type.split("PART-TIME")
        split_two = employee_type.split("PT")
        split_three = employee_type.split("SCHOOL X'ING GUAR")

        if len(split) > 1 or len(split_two) > 1 or len(split_three) > 1:
            return "Part-time, annual salary"
        return "Annual salary"

    @property
    def job_title(self):
        title = self.get_mapped_value('job_title').title().split("-",1)[1]
        split = title.split('Ii')
        split_two = title.split('Iv')
        split_three = title.split(' V')

        if len(split) == 1 and len(split_two) == 1 and len(split_three) == 1:
            return title
        elif len(split) > 1:
            return split[0] + ' II' + split[1]
        elif len(split_two) > 1:
            return split_two[0] + ' IV'
        elif len(split_three) > 1:
            return split_three[0] + ' V'

        return title

    @property
    def department(self):
        dept = self.get_mapped_value('department').title()
        split = dept.split('Itsd')
        split_two = dept.split("'S")

        if len(split) == 1 and len(split_two) == 1:
            return dept
        elif len(split) > 1:
            return dept.replace("Itsd","ItSD")
        elif len(split_two) > 1:
            return dept.replace("'S","'s")

        return dept

    @property
    def race(self):
        race = self.get_mapped_value('nationality').strip().title()
        split = race.split('Nonhispanic/Lat')
        split_two = race.split('(Non His)')
        split_three = race.split('Or')

        if len(split) == 1 and len(split_two) == 1 and len(split_three) == 1:
            return {
                'name': race
            }
        elif len(split) > 1:
            return {
                'name': race.replace('Or','or').replace('Nonhispanic/Lat','Non Hispanic or Latino')
            }
        elif len(split_two) > 1:
            return {
                'name': race.replace('Or','or').replace('(Non His)','(Non Hispanic)')
            }
        elif len(split_three) > 1:
            return {
                'name': race.replace('Or','or')
            }

transform = base.transform_factory(TransformedRecord)
