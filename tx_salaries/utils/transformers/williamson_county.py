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
        'first_name': 'EMPLOYEE FIRST NAME ',
        'last_name': 'EMPLOYEE LAST NAME       ',
        'job_title': 'POSITION                           ',
        'department': 'ORGANIZATION                  ',
        'gender_type': 'GENDER',
        'compensation_type': 'EMPLOYMENT CAT',
        'hire_date': 'ORIGINAL HIRE DT',
        'compensation': 'ANNUAL_SALARY  '
    }

    # The order of the name fields to build a full name.
    # If `full_name` is in MAP, you don't need this at all.
    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE, so double check it!
    ORGANIZATION_NAME = 'Williamson County'

    # What type of organization is this? This MUST match what we use on the site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'County'

    # Y/M/D agency provided the data
    DATE_PROVIDED = date(2017, 3, 21)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'williamson_county/salaries/2017-03/'
           'salaries.xlsx')

    ethnicity_choices = ['HISPANIC', 'AM_IND_AL', 'ASIAN', 'BLK_AFR_AMER',
                         'HAW_OTH', 'WHITE', '2_OR_MORE']

    # Adjust to return False on invalid fields
    @property
    def is_valid(self):
        if self.first_name.strip() == '':
            self.first_name = 'Name'
            self.last_name = 'Redacted'

        return self.last_name.strip() != ''

    @property
    def person(self):
        name = self.get_name()

        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r
    
    @property
    def gender(self):
        gender = self.get_mapped_value('gender_type')

        if gender.strip() == '':
            return 'Not Given'
        else:
            return gender

    @property
    def job_title(self):
        title = self.get_mapped_value('job_title')
        title_pretty = title.split(" 1.",1)[0].split(".0",1)[0].split(".1",1)[0].split(".9",1)[0]

        return title_pretty


    @property
    def compensation_type(self):
        emptype = self.get_mapped_value('compensation_type')

        if emptype.strip() == 'FULLTIME' or emptype.strip() == 'FLE':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        emptype = self.get_mapped_value('compensation_type')

        if emptype.strip() == 'FULLTIME' or emptype.strip() == 'FLE':
            return 'Annual salary'
        else:
            return 'Part-time, annual salary'

    @property
    def race(self):
        ethnicities = []

        for choice in self.ethnicity_choices:
            if self.data[choice].strip() == "Y":
                if choice == 'AM_IND_AL':
                    ethnicities.append('American Indian')
                elif choice == 'BLK_AFR_AMER':
                    ethnicities.append('Black')
                elif choice == 'HAW_OTH':
                    ethnicities.append('Pacific Islander')
                elif choice == '2_OR_MORE':
                    ethnicities.append('Two or more')
                else:
                    ethnicities.append( choice.title() )
        
        ethnicity = ", ".join(ethnicities)

        if ethnicity == '':
            ethnicity = 'Not given'
        
        # print ethnicity.strip()

        return {
            'name': ethnicity.strip()
        }

transform = base.transform_factory(TransformedRecord)
