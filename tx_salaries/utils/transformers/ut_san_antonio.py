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
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'AMIND': 'AMIND',
        'ASIAN': 'ASIAN',
        'BLACK': 'BLACK',
        'HISPA': 'HISPA',
        'NSPEC': 'NSPEC',
        'PACIF': 'PACIF',
        'WHITE': 'WHITE',
        'gender': 'Gender',
        'compensation': 'Rate',
        'status': 'Full/Part',
        'employment_frequency': 'Freq'
    }

    race_map = {
        'AMIND': 'American Indian or Alaskan Native',
        'ASIAN': 'Asian',
        'BLACK': 'Black or African American',
        'HISPA': 'Hispanic or Latino',
        'NSPEC': 'Not specified',
        'PACIF': 'Native Hawaiian or Pacific Islander',
        'WHITE': 'White'
    }

    # How do they track gender? We need to map what they use to `F` and `M`.
    # gender_map = {u'F': u'F', u'M': u'M', u'U': u'Unknown'}

    ORGANIZATION_NAME = 'University of Texas at San Antonio'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2015, 10, 7)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/ut_san_antonio/'
            'salaries/2015-10/utsanantonio.xls')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation(self):
        if not self.get_mapped_value('compensation'):
            return 0
        return self.get_mapped_value('compensation')

    @property
    def compensation_type(self):
        emp_type = self.status

        if emp_type == 'F':
            return 'FT'

        if emp_type == 'P':
            return 'PT'

    @property
    def description(self):
        emp_type = self.status
        freq = self.employment_frequency

        if freq == 'A':
            if emp_type == 'P':
                return "Part-time annual salary"
            return "Annual salary"

        if freq == 'H':
            return "Hourly rate"

        if freq == 'C':
            return "Contract salary"

    @property
    def race(self):
        races = [self.AMIND,self.ASIAN,self.BLACK,self.HISPA,self.NSPEC,self.PACIF,self.WHITE]
        raceNames = ['AMIND','ASIAN','BLACK','HISPA','NSPEC','PACIF','WHITE']
        i = 0
        raceList = []

        for indivRace in races:
            if indivRace == u'1':
                raceList.append(self.race_map[raceNames[i].strip()])
            i += 1

        if len(raceList) > 1:
            return {
                'name': 'Two or more races'
            }
        elif len(raceList) == 0:
            return {
                'name': 'Not given'
            }
        else:
            return {
                'name': raceList[0]
            }

    @property
    def person(self):
        name = self.get_name()
        gender = self.get_mapped_value('gender')
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
        }

        if gender.split() == 'U':
            gender = 'Unknown'
        r['gender'] = gender.split()

        return r

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
