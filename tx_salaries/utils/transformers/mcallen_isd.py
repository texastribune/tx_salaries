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
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'POSITION DESC',
        'hire_date': 'Most Recent Hire Date',
        'compensation': 'Contract Salary',
        'gender': 'Gender',
        'race': 'RACE',
        'status': 'Type'
    }

    # The name of the organization this WILL SHOW UP ON THE SITE,
    #  so double check it!
    ORGANIZATION_NAME = 'McAllen ISD'

    # What type of organization is this? This MUST match what we use on the
    # site, double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'School District'

    # How would you describe the compensation field? We try to respect how
    # they use their system.
    description = 'Salary'

    ORGANIZATION_MAP = {
        '001': "MCALLEN HIGH SCHOOL",
        '002': 'MEMORIAL HIGH SCHOOL',
        '005': 'INSTRUCTION AND GUIDANCE CENTER',
        '006': 'NIKKI ROWE HIGH SCHOOL',
        '007': 'OPTIONS IN EDUCATION/LAMAR ACADEMY',
        '011': 'EARLY COLLEGE HIGH SCHOOL',
        '042': 'TRAVIS MIDDLE SCHOOL',
        '043': 'LINCOLN MIDDLE SCHOOL',
        '045': 'BROWN MIDDLE SCHOOL',
        '046': 'MORRIS MIDDLE SCHOOL',
        '047': 'CATHEY MIDDLE SCHOOL',
        '048': 'FOSSUM MIDDLE SCHOOL',
        '101': 'ALVAREZ ELEMENTARY SCHOOL',
        '103': 'BONHAM ELEMENTARY SCHOOL',
        '106': 'HOUSTON ELEMENTARY SCHOOL',
        '107': 'JACKSON ELEMENTARY SCHOOL',
        '108': 'NAVARRO ELEMENTARY SCHOOL',
        '111': 'MILAM ELEMENTARY SCHOOL',
        '112': 'WILSON ELEMENTARY SCHOOL',
        '114': 'FIELDS ELEMENTARY SCHOOL',
        '116': 'SEGUIN ELEMENTARY SCHOOL',
        '119': 'ESCANDON ELEMENTARY SCHOOL',
        '120': 'RAYBURN ELEMENTARY SCHOOL',
        '121': 'ROOSEVELT ELEMENTARY SCHOOL',
        '122': 'GARZA ELEMENTARY SCHOOL',
        '123': 'MCAULIFFE ELEMENTARY SCHOOL',
        '124': 'GONZALEZ ELEMENTARY SCHOOL',
        '126': 'CASTANEDA ELEMENTARY SCHOOL',
        '127': 'SANCHEZ ELEMENTARY SCHOOL',
        '128': 'PEREZ ELEMENTARY SCHOOL',
        '129': 'HENDRICKS ELEMENTARY SCHOOL',
        '130': 'THIGPEN/ZAVALA ELEMENTARY SCHOOL',
        '699': 'SUMMER SCHOOL',
        '701': 'SUPERINTENDENT\'S OFFICE',
        '702': 'BOARD OF TRUSTEES',
        '703': 'DEPARTMENT OF TAX ASSESSOR/COLLECTOR',
        '713': 'GRANT DEVELOPMENT AND COMPLIANCE',
        '714': 'DEPARTMENT OF COMMUNITY INFORMATION',
        '716': 'DEPARTMENT OF INSTRUCTIONAL MATERIALS & STUDENT RECORDS',
        '727': 'DEPARTMENT OF HUMAN RESOURCES',
        '728': 'DEPARTMENT OF EMPLOYEE BENEFITS',
        '729': 'DEPARTMENT OF PURCHASING',
        '730': 'DIVISION OF BUSINESS SERVICES',
        '731': 'ASSISTANT SUPERINTENDENT FOR DISTRICT OPERATIONS',
        '732': 'DEPARTMENT OF INTERNAL AUDIT',
        '733': 'ASSISTANT SUPERINTENDENT FOR BUSINESS OPERATIONS',
        '751': 'FISCAL AGENT SHARED SERVICES ARRANGEMENTS',
        '800': 'WAREHOUSE/FIXED ASSETS',
        '801': 'POLICE DEPARTMENT',
        '802': 'DIVISION OF INSTRUCTION',
        '803': 'DEPARTMENT OF STUDENT SUPPORT SERVICES',
        '804': 'DEPARTMENT OF ATHLETICS',
        '805': 'DEPARTMENT OF FINE ARTS',
        '807': 'DEPARTMENT OF TECHNOLOGY',
        '808': 'FACILITIES MAINTENANCE & OPERATIONS',
        '809': 'DEPARTMENT OF TRANSPORTATION',
        '810': 'DEPARTMENT OF FOOD SERVICE',
        '811': 'DEPARTMENT OF INSTRUCTIONAL TECHNOLOGY',
        '812': 'DEPARTMENT OF MEDIA SERVICES',
        '813': 'DEPARTMENT OF LIBRARY SERVICES',
        '814': 'DEPARTMENT OF SPECIAL EDUCATION SERVICES',
        '815': 'DEPARTMENT OF HEALTH SERVICES',
        '816': 'WELLNESS PROGRAM',
        '817': 'DEPARTMENT OF SPECIAL SERVICES',
        '819': 'DEPARTMENT OF RESEARCH AND POLICY',
        '998': 'UNALLOCATED',
        '999': 'SUBSTITUTE'
    }

    RACE_MAP = {
        '1': 'American Indian/Alaska Native',
        '2': 'Asian',
        '3': 'Black or African American',
        '4': 'Native Hawaiian or Other Pacific Islander',
        '5': 'White'
    }

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 2, 20)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://raw.texastribune.org.s3.amazonaws.com/'
           'dallas_isd/salaries/2015-11/dallas_isd.xlsx')

    # This is how the loader checks for valid people. Defaults to checking to
    # see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.job_title.strip() != 'STADIUM WORKER'

    # @property
    # def hire_date(self):
    #     raw_date = self.get_mapped_value('hire_date')
    #     return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

    @property
    def compensation_type(self):
        emp_type = self.status

        if emp_type == 'E':
            return 'FT'

        if emp_type == 'SU':
            return 'PT'

        if emp_type == 'PTRT':
            return 'PT'

        if emp_type == 'RTTH':
            return 'FT'

        if emp_type == 'SURT':
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
            'gender': self.gender
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
