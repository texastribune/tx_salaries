from . import base
from . import mixins

from datetime import date, datetime


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'full_name': 'Name',
        'department_code': 'Department',
        'job_title': 'POSITION DESC',
        'hire_date': 'Most Recent Hire Date',
        'compensation': 'Contract Salary',
        'gender': 'Gender',
        'ethnicity': 'RACE',
        'status': 'Type',
        'unique': 'ID'
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

    DEPARTMENT_MAP = {
        '001': 'MCALLEN HIGH SCHOOL',
        '002': 'MEMORIAL HIGH SCHOOL',
        '005': 'INSTRUCTION AND GUIDANCE CENTER',
        '006': 'NIKKI ROWE HIGH SCHOOL',
        '007': 'OPTIONS IN EDUCATION/LAMAR ACADEMY',
        '011': 'EARLY COLLEGE HIGH SCHOOL',
        '042': 'TRAVIS MIDDLE SCHOOL',
        '043': 'LINCOLN MIDDLE SCHOOL',
        '044': 'BROWN MIDDLE SCHOOL',
        '045': 'MORRIS MIDDLE SCHOOL',
        '046': 'DE LEON MIDDLE SCHOOL',
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
        '999': 'SUBSTITUTE',
        '180': '',
        '100': '',
        '104': ''
    }

    race_map = {
        '1': 'American Indian/Alaska Native',
        '2': 'Asian',
        '3': 'Black or African American',
        '4': 'Native Hawaiian or Other Pacific Islander',
        '5': 'White'
    }

    # When did you receive the data? NOT when we added it to the site.
    DATE_PROVIDED = date(2017, 2, 20)

    # The URL to find the raw data in our S3 bucket.
    URL = ('http://s3.amazonaws.com/raw.texastribune.org/'
           'mcallen_isd/salaries/2017-02/mcallen_isd.xlsx')

    # This is how the loader checks for valid people. Defaults to checking to
    # see if `last_name` is empty.
    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        # return self.get_mapped_value('full_name').strip() != ''
        return self.get_mapped_value("compensation") != 0

    def process_compensation(self):
        raw_compensation = self.get_mapped_value("compensation")
        return float(raw_compensation)

    # @property
    # def identifier(self):
    #     return {
    #         'scheme': 'tx_salaries_hash',
    #         'identifier': base.create_hash_for_record(self.data,
    #                 exclude=[self.compensation_key, ])
    #     }

    @property
    def department(self):
        departmentCode = self.DEPARTMENT_MAP[self.get_mapped_value("department_code").strip()[:3]]
        return departmentCode

    @property
    def race(self):
        return {
            'name': self.race_map[self.get_mapped_value("ethnicity").strip()]
        }

    @property
    def compensation_type(self):
        emp_type = self.get_mapped_value("status")
        # full-time employee
        if emp_type == 'E':
            return 'FT'
        elif emp_type == 'SU':
            # substutites
            return 'PT'
        elif emp_type == 'PT':
            return 'PT'
        elif emp_type == 'PTRT':
            # part time retured teacher - retired teacher who was rehired
            # as a part-time employee
            return 'PT'
        elif emp_type == 'RTRH':
            # retired reacher who was rehired full-time
            return 'FT'
        elif emp_type == 'SURT':
            # substitute teacher who is also a retired teacher
            return 'PT'

    @property
    def hire_date(self):
        raw_hire_date = self.get_mapped_value('hire_date')
        parsed_hire_date = map(int, raw_hire_date.split('/'))

        return '-'.join([
            str(i) for i in
            [parsed_hire_date[2], parsed_hire_date[0], parsed_hire_date[1]]
        ])

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
        split_name = self.get_mapped_value('full_name').split(', ')
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
